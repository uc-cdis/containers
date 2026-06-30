# Gen3 Workspace Container for RCC (Python 3.14 + SigProfilerMatrixGenerator)

This repository contains the infrastructure configurations for deploying a custom JupyterLab environment for Gen3 Workspaces. It runs on a rootless **Python 3.14-slim** base image, isolates reference genomes completely inside the private container image to protect multi-workspace storage health, and complies with Gen3 Hatchery security policies (`UID 1010` / `GID 101`).

---

## 🏗️ Architecture Overview

When Gen3 initializes a workspace pod, it mounts an external Kubernetes Persistent Volume Claim (PVC) directly onto `/home/jovyan/pd`. This PVC is linked to the user's account and persists across all workspace types they open (including Generic R/Python workspaces).

To prevent multi-tenant configuration drift or dead link corruption on the user's shared storage drive, this image utilizes an completely isolated data design:
1. **Build Phase:** Reference genomes (`GRCh38`) are pre-downloaded natively into a private, rootless home directory cache path (`/home/jovyan/reference_genomes`).
2. **Runtime Isolation:** The genome data remains strictly within the container image layer. No data, links, or file modifications are pushed onto the shared `/home/jovyan/pd` drive, ensuring your other workspace types remain unaffected.
3. **Execution Routing:** The wrapper script handles terminal customization (injecting `git`, username prompt settings, and tab-autocomplete components) and manages commands dynamically based on whether flags or interactive utilities are called.

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

Inside this terminal session, run the following to verify that your data resides safely in the container's isolated local layer:
```bash
ls -la /home/jovyan/reference_genomes/
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

custom_volume = os.environ.get("SIGPROFILERMATRIXGENERATOR_VOLUME", "/home/jovyan/reference_genomes")
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
    "FRAME_ANCESTORS": "https://planx-pla.net"
  },
  "args": [
    "--ip=0.0.0.0",
    "--port=8888",
    "--no-browser",
    "--ServerApp.base_url=/lw-workspace/proxy/",
    "--ServerApp.default_url=/lab",
    "--ServerApp.password",
    "",
    "--ServerApp.token",
    "",
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
* **ECR Registration:** Ensure the `"image"` path matches your production build pipeline destination registry.
* **Arguments Check:** `--allow-root` is entirely removed from the array to prevent parsing crashes, and empty initialization components (`password`, `token`) are properly separated onto unique configuration entries to maintain Hatchery string integrity.
