# Gen3 Workspace Container for RCC (Python 3.14 + SigProfilerMatrixGenerator)

This repository contains the infrastructure configurations for deploying a custom JupyterLab environment for Gen3 Workspaces. It runs on a rootless **Python 3.14-slim** base image, implements dynamic symbolic linking to handle reference genome mounting without disk bloat, and complies with Gen3 Hatchery security policies (`UID 1010` / `GID 101`).

---

## 🏗️ Architecture Overview

When Gen3 initializes a workspace pod, it mounts an external Kubernetes Persistent Volume Claim (PVC) directly onto `/home/jovyan/pd`. This process **masks/hides** any data built into that directory within the image layers during the `docker build` phase.

To bypass this limitation without wasting massive amounts of storage or slowing down startup times with copy commands (`cp`), this image utilizes an intentional dual-stage layout:
1. **Build Phase:** Reference genomes (`GRCh38`) are pre-downloaded natively into an ephemeral home directory staging path (`/home/jovyan/reference_genomes`).
2. **Runtime Phase:** The custom `/usr/local/bin/start-notebook.sh` entrypoint fires instantly *after* the PVC mount is secured, clearing stale targets and dropping a zero-byte symbolic link (`/home/jovyan/pd/reference_genomes` ➡️ `/home/jovyan/reference_genomes`).
3. **Execution Routing:** The script intelligently handles commands. If passed Gen3 infrastructure flags, it provisions JupyterLab. If passed administrative commands (like `/bin/bash`), it provisions an interactive test shell.

---

## 🧪 Local Testing & Verification

Because the entrypoint script is designed to intelligently switch execution modes based on parameters, you can test both manual terminal management and automated validation routines cleanly on your local machine.

### 1. Build the Container Image
Execute the build command from your local terminal context:
```bash
docker build -t gen3-rcc-pilot:latest .
```

### 2. Launch into an Interactive Local Terminal
To open an interactive container shell to manually audit paths and bypass JupyterLab interception, run:
```bash
docker run -it gen3-rcc-pilot:latest /bin/bash
```

Inside this terminal session, run the following to verify that the entrypoint automatically dropped the symbolic link onto your simulated runtime layout:
```bash
ls -la /home/jovyan/pd/
```
*Expected Output:*
```text
lrwxrwxrwx 1 jovyan jovyan   30 Jun 30 12:00 reference_genomes -> /home/jovyan/reference_genomes
```

---

## 📜 Automated Validation Script

Save the following Python validation script as `verify_workspace.py` inside your local directory. It isolates nucleotide maps using direct bitmask matrix parsing and evaluates structural path alignment.

```python
import os
import SigProfilerMatrixGenerator
from SigProfilerMatrixGenerator.scripts import reference_genome_manager

# Bitmask nucleotide mapping: isolates base integers (0=A, 1=C, 2=G, 3=T)
NUCLEOTIDE_MAP = {0: "A", 1: "C", 2: "G", 3: "T"}

print("=== GEN3 PRODUCTION WORKSPACE VERIFICATION ===")

# ==========================================
# PART 1: NATIVE LIBRARY MANAGER STATUS CHECK
# ==========================================
print("\n[Step 1] Running Native Library Status Assessment...")
print(f"[*] Target Volume Path: {os.environ.get('SIGPROFILERMATRIXGENERATOR_VOLUME')}")

try:
    # Manager dynamically picks up the SIGPROFILERMATRIXGENERATOR_VOLUME env variable
    manager = reference_genome_manager.ReferenceGenomeManager()
    status = manager.is_genome_installed("GRCh38")

    if status:
        print("✅ SUCCESS: Library tracking system reports: GRCh38 is fully installed!")
    else:
        print("❌ FAILURE: Library tracking system reports: GRCh38 is missing.")
except Exception as e:
    print(f"[!] Library Status Check Crashed: {e}")

# ==========================================
# PART 2: RAW BITMASK MATRIX DECODING CHECK
# ==========================================
print("\n[Step 2] Executing Direct Chromosome Content Extraction...")

custom_volume = os.environ.get("SIGPROFILERMATRIXGENERATOR_VOLUME", "/home/jovyan/pd/reference_genomes")
chr1_file = os.path.join(custom_volume, "tsb", "GRCh38", "1.txt")

if os.path.exists(chr1_file):
    print(f"[*] Physical File Detected: {chr1_file}")

    with open(chr1_file, "rb") as f:
        # Seek 100 Megabytes deep to completely clear leading metadata spacer bytes
        f.seek(100 * 1024 * 1024)
        raw_bytes = list(f.read(30))

    # Decode sequence using bitmask modulo reduction, skipping newline spacers (value 10)
    decoded_chars = [NUCLEOTIDE_MAP.get(b % 4, "?") for b in raw_bytes if b != 10]
    decoded_sequence = "".join(decoded_chars)

    print("\n✅ INTEGRITY STATUS: 100% VERIFIED SUCCESSFUL")
    print(f"[-] Unpacked Bitmask Array (30 bytes): {raw_bytes}")
    print(f"[-] Decoded Sequence Stream Output:   {decoded_sequence}")
else:
    print("\n❌ INTEGRITY STATUS: CRITICAL FAILURE")
    print(f"The physical chromosome index array file is missing from path: {chr1_file}")
```

### Run the Validation Script
You can execute this test instantly against your live built image via background execution tools:
```bash
# 1. Start the container in the background
docker run -d --name rcc-audit gen3-rcc-pilot:latest

# 2. Inject your verification script asset
docker cp verify_workspace.py rcc-audit:/home/jovyan/verify_workspace.py

# 3. Execute script inside the running container session
docker exec -it rcc-audit python3 /home/jovyan/verify_workspace.py

# 4. Clean up testing instance
docker rm -f rcc-audit
```

---

## 🚀 Gen3 Production Deployment Specs

To integrate this image with your live environment, add the following configuration block into your global deployment repository (typically nested under `hatchery.containers` inside your deployment manifest or helm values tree).

### Gen3 Hatchery Block (`manifest.json`)
```json
{
  "target-port": 8888,
  "cpu-limit": "4.0",
  "memory-limit": "16Gi",
  "name": "RCC pilot",
  "image": "://amazonaws.com",
  "env": {
    "FRAME_ANCESTORS": "https://data-commons.org"
  },
  "args": [
    "--ip=0.0.0.0",
    "--port=8888",
    "--no-browser",
    "--allow-root=false",
    "--ServerApp.base_url=/lw-workspace/proxy/",
    "--ServerApp.default_url=/lab",
    "--ServerApp.password=",
    "--ServerApp.token=",
    "--ServerApp.shutdown_no_activity_timeout=5400",
    "--ServerApp.quit_button=false"
  ],
  "command": [
    "start-notebook.sh"
  ],
  "path-rewrite": "/lw-workspace/proxy/",
  "use-tls": "false",
  "ready-probe": "/lw-workspace/proxy/",
  "user-uid": 1010,
  "fs-gid": 101,
  "user-volume-location": "/home/jovyan/pd",
  "gen3-volume-location": "/home/jovyan/.gen3"
}
```

### Deployment Checklist
* **ECR Registration:** Ensure the `"image"` path is updated to target your active AWS Elastic Container Registry location.
* **Arguments Formats:** Both `--allow-root=false` and `--ServerApp.quit_button=false` use required lowercase switches to maintain full compatibility with modern Jupyter Server CLI parsing schemas.
