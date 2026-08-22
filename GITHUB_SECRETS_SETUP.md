# GitHub Secrets Setup for CI/CD with NVIDIA GPU

## Required GitHub Repository Secrets

Go to: `https://github.com/goodwearrinfo-aryan/AgentsSwarm/settings/secrets/actions`

### 1. NVIDIA API Key (for GPU inference/NIM)
```
Name: NVIDIA_API_KEY
Value: nvapi-xxxxxxxxxxxxxxxxxxxxxxxx (your NVIDIA NGC API key)
```
Get from: https://ngc.nvidia.com/setup/api-key

### 2. GCP VM Deployment (staging/production)
```
Name: STAGING_VM_HOST
Value: <staging-vm-external-ip>

Name: STAGING_VM_USER
Value: <ssh-username> (e.g., ubuntu)

Name: STAGING_VM_SSH_KEY
Value: <private-ssh-key-content> (-----BEGIN OPENSSH PRIVATE KEY----- ...)
```

```
Name: VM_HOST
Value: <production-vm-external-ip>

Name: VM_USERNAME
Value: <ssh-username>

Name: VM_SSH_KEY
Value: <private-ssh-key-content>
```

### 3. Supabase (for backend)
```
Name: SUPABASE_URL
Value: https://your-project.supabase.co

Name: SUPABASE_SERVICE_KEY
Value: <service-role-key>

Name: SUPABASE_JWT_SECRET
Value: <jwt-secret>
```

### 4. Firebase
```
Name: FIREBASE_PROJECT_ID
Value: <your-firebase-project-id>
```

### 5. LLM Provider Keys (optional - for GPU workers)
```
Name: GROQ_API_KEY
Value: gsk_xxxxxxxxxxxxxxxx

Name: GEMINI_API_KEY
Value: <gemini-api-key>

Name: ELEVENLABS_API_KEY
Value: <elevenlabs-api-key>

Name: SERPER_API_KEY
Value: <serper-api-key>
```

## NVIDIA GPU Runner Options

### Option A: Self-hosted GPU Runner (Recommended for control)
```bash
# On your GPU machine (with NVIDIA driver + Docker + nvidia-container-toolkit):
# 1. Install GitHub Actions runner
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.317.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.317.0/actions-runner-linux-x64-2.317.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.317.0.tar.gz
./config.sh --url https://github.com/goodwearrinfo-aryan/AgentsSwarm --token <runner-token> --labels linux,gpu,nvidia
./run.sh
```

### Option B: GitHub-hosted GPU Runners (Enterprise only)
- Available on GitHub Enterprise Cloud with "GitHub-hosted larger runners"
- Use `runs-on: ubuntu-latest-4-gpu` or `ubuntu-latest-8-gpu`
- Requires billing setup

### Option C: Cloud GPU Instances (AWS/Azure/GCP)
- Spin up GPU instances on demand via Actions
- Use `aws-actions/configure-aws-credentials` + custom runner registration

## Docker Registry (GHCR)
Images are pushed to `ghcr.io/goodwearrinfo-aryan/AgentsSwarm/backend:latest`
- Public by default (change in package settings if needed)
- Pull with: `docker pull ghcr.io/adi-3108/agentsswarm/backend:latest`

## Local Development with GPU
```bash
# Build GPU image locally
docker build -f backend/Dockerfile.gpu -t agentsswarm/backend:gpu .

# Run with GPU
docker run --rm --gpus all -p 8000:8000 \
  -e NVIDIA_API_KEY=$NVIDIA_API_KEY \
  agentsswarm/backend:gpu
```

## Workflow Files
- `.github/workflows/ci.yml` - Main CI (test, build, GPU test, deploy)
- `.github/workflows/gpu-build.yml` - GPU-specific Docker build
- `.github/workflows/codeql.yml` - Security scanning
- `.github/workflows/deploy-vm.yml` - GCP VM deployment
