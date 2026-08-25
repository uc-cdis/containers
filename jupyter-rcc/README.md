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
ls -la /home/jovyan/reference_genomes/tsb
```

---

## 📜 Automated Validation Script

There is Python validation script `verify_workspace.py` inside this repository. It validates if GRCh38 genome reference was installed properly.

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
  "pull_policy": "Always",
  "env": {
    "FRAME_ANCESTORS": "https://planx-pla.net"
  },
  "args": [
    "--ip=0.0.0.0",
    "--port=8888",
    "--no-browser",
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
* Ensure the `"image"` path matches your image destination
* Ensure the `"FRAME_ANCESTORS"` URL matches your data commons URL
