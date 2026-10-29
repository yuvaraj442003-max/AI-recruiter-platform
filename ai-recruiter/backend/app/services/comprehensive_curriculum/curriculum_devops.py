"""
curriculum_devops.py - Complete 8 Chapters Comprehensive Curriculum for DevOps.
Every chapter contains:
1. Detailed Concepts & In-Depth Explanation
2. Key Formulas, Rules & Architecture
3. Step-by-Step Solved Examples with working code and breakdown
4. Practice Questions with Answers & Explanations
5. Company Placement Technical Interview Questions & Answers
"""
from typing import List, Dict, Any

DEVOPS_CHAPTERS: List[Dict[str, Any]] = [
    {
        "chapter_num": 1,
        "title": "DevOps Culture, CALMS Framework, Git Workflows & Trunk-Based Development",
        "key_takeaways": "Master the CALMS framework, DORA metrics, Git branching strategies (GitFlow vs Trunk-Based), and semantic versioning.",
        "topics": [
            "DevOps Philosophy: Breaking silos between Development, QA & Operations",
            "CALMS Framework: Culture, Automation, Lean, Measurement, Sharing",
            "DORA Metrics: Deployment Frequency, Lead Time for Changes, Change Failure Rate, Time to Restore Service",
            "Git Workflows: GitFlow vs GitHub Flow vs Trunk-Based Development with Feature Flags",
            "Semantic Versioning (SemVer 2.0.0): Major.Minor.Patch rules and release tagging"
        ],
        "sections": {
            "concept": "DevOps combines cultural philosophies, practices, and tools to increase an organization's velocity in delivering applications. The CALMS framework emphasizes Culture, Automation, Lean product flow, Measurement, and Sharing knowledge. High-performing engineering teams measure success via the four DORA (DevOps Research and Assessment) metrics. While GitFlow was designed for scheduled desktop releases with long-lived feature and release branches, modern cloud-native teams favor Trunk-Based Development: all developers commit small, frequent increments directly to the main trunk daily, decoupling deployment from release using Feature Flags.",
            "formulas": "1. Change Failure Rate (CFR) = (Failed_Deployments / Total_Deployments) * 100\n2. Lead Time for Changes = Time elapsed from first git commit to running in production\n3. DORA Elite Standard: Deploy Multiple times/day, Lead Time < 1 hour, CFR < 5%, MTTR < 1 hour",
            "solved_examples": [
                {
                    "title": "Implementing Feature Flags to Decouple Deployment from Release",
                    "difficulty": "Easy | Spotify, Netflix, Microsoft",
                    "problem": "Write a clean Python feature flag evaluation function that safely enables a new AI checkout flow for 10% of users without branch merging.",
                    "step_by_step": [
                        "Step 1: Hash the user's unique ID with salt using MD5 or MurmurHash3.",
                        "Step 2: Map hash to integer modulo 100 (bucket range 0-99).",
                        "Step 3: If bucket < rollout_percentage, return True (enable feature).",
                        "Step 4: All other users execute the stable baseline flow.",
                        "Step 5: Code is merged to main trunk and deployed to production continuously without exposing incomplete features."
                    ],
                    "code_or_math": "import hashlib\n\ndef is_feature_enabled(user_id, feature_name, rollout_pct=10):\n    key = f'{feature_name}:{user_id}'\n    hash_val = int(hashlib.md5(key.encode()).hexdigest(), 16)\n    bucket = hash_val % 100\n    return bucket < rollout_pct\n\nprint('User 1042 feature active:', is_feature_enabled(1042, 'ai_checkout', 10))"
                }
            ],
            "practice_questions": [
                {
                    "question": "Which DORA metric measures the percentage of production deployments that cause a service outage or require an emergency rollback?",
                    "options": [
                        "Deployment Frequency",
                        "Lead Time for Changes",
                        "Change Failure Rate (CFR)",
                        "Mean Time to Inspect"
                    ],
                    "answer": "Change Failure Rate (CFR)",
                    "explanation": "Change Failure Rate measures the proportion of releases that result in degraded service or unexpected failures requiring hotfixes, rollbacks, or patches in production."
                }
            ],
            "interview_questions": [
                {
                    "company": "Netflix & Microsoft",
                    "question": "Why do high-performing engineering teams prefer Trunk-Based Development over GitFlow?",
                    "model_answer": "GitFlow relies on long-lived feature branches, release branches, and develop branches that diverge over weeks, resulting in painful 'merge hell', complex rebasing, and delayed integration feedback. Trunk-Based Development mandates committing small, tested code batches to the main trunk daily. Paired with automated CI pipelines and Feature Flags, it shortens feedback loops, eliminates merge conflicts, and enables continuous daily deployments.",
                    "interviewer_tip": "Connect trunk-based development directly to short lead times and continuous testing."
                }
            ]
        }
    },
    {
        "chapter_num": 2,
        "title": "Continuous Integration & Delivery (CI/CD): Jenkins, GitHub Actions & GitLab CI",
        "key_takeaways": "Master declarative pipeline construction, automated build/test/package phases, secret handling, and artifact registries.",
        "topics": [
            "Continuous Integration (CI) vs Continuous Delivery (CD) vs Continuous Deployment",
            "GitHub Actions: Workflows, Triggers (push, pull_request), Jobs, Matrix builds & Runners",
            "Jenkins Declarative Pipelines: Jenkinsfile syntax, stages, steps, post-actions & agents",
            "CI Security: Secret scanning, short-lived OIDC tokens for cloud auth & dependency auditing",
            "Artifact Repository Management: Storing Docker images, NPM packages & Python wheels in Harbor/Nexus/ECR"
        ],
        "sections": {
            "concept": "Continuous Integration (CI) is the practice of automatically building and testing code on every single commit. Continuous Delivery (CD) ensures the software is always in a deployable state, requiring manual approval to promote to production, while Continuous Deployment automatically deploys all passing builds to production without human intervention. Declarative pipelines define stages (Lint, Unit Test, Security Scan, Build, Package, Deploy). Modern CI systems authenticate with cloud providers using short-lived OpenID Connect (OIDC) tokens, eliminating static stored cloud credentials.",
            "formulas": "1. Pipeline Duration: T_pipeline = max(Parallel_Jobs) + Sum(Sequential_Stages)\n2. Test Flakiness % = (Inconsistent_Test_Runs / Total_Test_Runs) * 100\n3. Build Cache Speedup: Speedup = T_clean_build / T_cached_build",
            "solved_examples": [
                {
                    "title": "Writing a Production GitHub Actions CI/CD Pipeline for Docker Build and Test",
                    "difficulty": "Medium | GitHub, Microsoft, Stripe",
                    "problem": "Create a `.github/workflows/deploy.yml` pipeline that lints code, runs unit tests in parallel matrix, builds a Docker image, and caches layers.",
                    "step_by_step": [
                        "Step 1: Set triggers on push to main branch and pull requests.",
                        "Step 2: Configure matrix strategy to test across Python 3.11 and 3.12.",
                        "Step 3: Run pytest with test coverage thresholds.",
                        "Step 4: Use Docker Buildx with GitHub Actions cache for layer reuse.",
                        "Step 5: Authenticate to container registry using OIDC."
                    ],
                    "code_or_math": "name: CI/CD Pipeline\non:\n  push:\n    branches: [main]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    strategy:\n      matrix:\n        python-version: ['3.11', '3.12']\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n        with:\n          python-version: ${{ matrix.python-version }}\n      - run: pip install -r requirements.txt && pytest tests/\n  build:\n    needs: test\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: docker/setup-buildx-action@v3\n      - uses: docker/build-push-action@v5\n        with:\n          push: false\n          tags: app:${{ github.sha }}"
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the critical distinction between Continuous Delivery and Continuous Deployment?",
                    "options": [
                        "Continuous Delivery uses Jenkins; Continuous Deployment uses GitHub Actions",
                        "Continuous Delivery requires manual approval to promote to production; Continuous Deployment automatically deploys every passing commit to production",
                        "Continuous Deployment only runs on Windows servers",
                        "Continuous Delivery deletes all git history after deployment"
                    ],
                    "answer": "Continuous Delivery requires manual approval to promote to production; Continuous Deployment automatically deploys every passing commit to production",
                    "explanation": "In Continuous Delivery, every successful build is packaged and tested so it is always deployable, but human decision/approval triggers release to production. In Continuous Deployment, every change that passes the automated pipeline is automatically deployed to production with zero manual intervention."
                }
            ],
            "interview_questions": [
                {
                    "company": "GitLab & Atlassian",
                    "question": "How do modern CI/CD systems like GitHub Actions securely authenticate with AWS or Azure without storing permanent cloud access keys?",
                    "model_answer": "Modern CI/CD runners use OpenID Connect (OIDC). The runner requests a cryptographically signed JSON Web Token (JWT) from the CI identity provider. The runner presents this token to the cloud provider's STS (Security Token Service). The cloud provider verifies the JWT signature and claims (repository name, branch, environment), and issues temporary, short-lived IAM credentials that expire automatically after the build completes.",
                    "interviewer_tip": "Mention OIDC federation to demonstrate cutting-edge CI/CD security knowledge."
                }
            ]
        }
    },
    {
        "chapter_num": 3,
        "title": "Containerization with Docker: Dockerfile Best Practices & Multi-Stage Builds",
        "key_takeaways": "Master Linux kernel namespaces/cgroups, Docker layer caching, distroless minimal images, container networking, and security best practices.",
        "topics": [
            "Linux Container Internals: Namespaces (pid, net, mnt, ipc, uts) and Control Groups (cgroups v2)",
            "Dockerfile Best Practices: Layer caching, order of instructions, .dockerignore & non-root users",
            "Multi-Stage Docker Builds: Separating build toolchains from lean runtime images",
            "Container Networking: Bridge, Host, Overlay & Macvlan network drivers",
            "Container Security: Vulnerability scanning (Trivy), read-only root filesystems & seccomp profiles"
        ],
        "sections": {
            "concept": "Docker packages applications and dependencies into standardized containers sharing the host OS kernel. Containers are isolated using Linux kernel primitives: Namespaces provide isolated views of system resources (process IDs, network interfaces, filesystem mount points); Control Groups (cgroups) limit and measure CPU, RAM, and I/O consumption. Every instruction in a Dockerfile creates an immutable read-only layer. Multi-stage builds compile code inside heavy builder images (containing compilers, SDKs, and build dependencies) and copy only the final binary into a minimal distroless or Alpine runtime image, reducing image sizes from 1 GB+ down to under 50 MB.",
            "formulas": "1. Container Memory Limit: cgroup memory.max = Hard_Limit_Bytes (Triggers OOM Killer if exceeded)\n2. Image Layer Size Reduction: Multi-Stage Build typical size reduction: 90% to 95%\n3. OverlayFS Storage: Merged = LowerDir (Read-Only Images) + UpperDir (Container Read-Write) + WorkDir",
            "solved_examples": [
                {
                    "title": "Writing a Production Multi-Stage Dockerfile for Python / Go Application",
                    "difficulty": "Medium | Docker, Google, Amazon",
                    "problem": "Create a hardened, non-root, minimal multi-stage Dockerfile that packages a Python FastAPI microservice.",
                    "step_by_step": [
                        "Step 1: Stage 1 (Builder): Use `python:3.11-slim` to compile wheels and dependencies.",
                        "Step 2: Stage 2 (Runner): Start from fresh `python:3.11-slim`.",
                        "Step 3: Create dedicated non-root system user and group (`appuser:1001`).",
                        "Step 4: Copy installed wheels from builder stage.",
                        "Step 5: Set `USER appuser` and define `HEALTHCHECK` probe and unbuffered environment flags."
                    ],
                    "code_or_math": "# Multi-Stage Production Dockerfile\nFROM python:3.11-slim AS builder\nWORKDIR /app\nRUN apt-get update && apt-get install -y --no-install-recommends gcc\nCOPY requirements.txt .\nRUN pip install --no-cache-dir --user -r requirements.txt\n\nFROM python:3.11-slim AS runner\nWORKDIR /app\nRUN groupadd -g 1001 appgroup && useradd -u 1001 -g appgroup -s /bin/false appuser\nCOPY --from=builder /root/.local /home/appuser/.local\nCOPY . .\nENV PATH=/home/appuser/.local/bin:$PATH PYTHONUNBUFFERED=1\nUSER appuser\nHEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health || exit 1\nCMD ['uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8000']"
                }
            ],
            "practice_questions": [
                {
                    "question": "Why should you order Dockerfile instructions so that frequently changing application code (e.g. `COPY . .`) is placed AFTER `COPY requirements.txt` and package installation?",
                    "options": [
                        "Because Linux kernels require source code at the bottom of the file",
                        "To maximize Docker layer caching: if dependencies haven't changed, Docker reuses cached layers and skips re-downloading packages",
                        "To prevent CSS styles from breaking",
                        "It is a mandatory syntactical requirement of Docker version 24"
                    ],
                    "answer": "To maximize Docker layer caching: if dependencies haven't changed, Docker reuses cached layers and skips re-downloading packages",
                    "explanation": "Docker evaluates build cache sequentially from top to bottom. If an instruction's inputs change, that layer and all subsequent layers must be rebuilt. Placing dependencies first allows Docker to reuse the cached dependencies layer whenever only application source code is modified."
                }
            ],
            "interview_questions": [
                {
                    "company": "Red Hat & Docker",
                    "question": "What is the difference between a virtual machine (VM) and a Docker container?",
                    "model_answer": "A virtual machine includes a full guest operating system, virtual device drivers, and hypervisor layer (Type 1 or 2), incurring significant memory overhead and taking minutes to boot. A container shares the underlying host operating system kernel directly, isolating processes via Linux kernel Namespaces and Cgroups. Containers boot in milliseconds, have near-native bare-metal execution speed, and consume a fraction of the memory footprint.",
                    "interviewer_tip": "Cite Namespaces and Cgroups as the technical underpinning of container isolation."
                }
            ]
        }
    },
    {
        "chapter_num": 4,
        "title": "Kubernetes (K8s) Cluster Architecture, Pods, Deployments & Networking",
        "key_takeaways": "Master the K8s control plane (API Server, etcd, Scheduler, Controller Manager), Pod lifecycles, Deployments, Services, and Ingress Controllers.",
        "topics": [
            "Kubernetes Control Plane vs Worker Node Architecture (kubelet, kube-proxy, container runtime)",
            "Core workload primitives: Pods, ReplicaSets, Deployments, StatefulSets & DaemonSets",
            "K8s Networking model: Pod-to-Pod communication (CNI: Calico, Flannel, Cilium)",
            "Services: ClusterIP (Internal), NodePort, LoadBalancer & Headless services",
            "Ingress Controllers (Nginx, Traefik), Ingress resources, Path-based routing & TLS termination"
        ],
        "sections": {
            "concept": "Kubernetes is the industry standard for automating container deployment, scaling, and operational management. The Control Plane consists of the kube-apiserver (REST interface), etcd (consistent distributed key-value store for cluster state), kube-scheduler (assigns pods to worker nodes based on resource requests/limits), and kube-controller-manager (enforces desired state). Worker nodes run kubelet (agent communicating with the API server) and kube-proxy (manages iptables/IPVS networking rules). Pods are the smallest deployable compute unit. Deployments manage declarative rolling updates and rollbacks across ReplicaSets.",
            "formulas": "1. Pod Resource Equation: Requests <= Usage <= Limits (Breaching CPU limit throttles; breaching RAM limit triggers OOMKilled)\n2. RollingUpdate Parameters: maxSurge (default 25%) and maxUnavailable (default 25%)\n3. etcd Consensus: Quorum = (N / 2) + 1 (A 3-node etcd cluster tolerates 1 node failure; 5-node tolerates 2)",
            "solved_examples": [
                {
                    "title": "Writing a Kubernetes Deployment Manifest with Rolling Update & Resource Constraints",
                    "difficulty": "Hard | Google, Amazon, Red Hat",
                    "problem": "Write a production Kubernetes Deployment YAML for a 3-replica backend API with liveness/readiness probes and CPU/RAM requests.",
                    "step_by_step": [
                        "Step 1: Set `apiVersion: apps/v1` and `kind: Deployment`.",
                        "Step 2: Define `replicas: 3` and matchLabels selector.",
                        "Step 3: Define `strategy: RollingUpdate` with `maxSurge: 1` and `maxUnavailable: 0` for zero-downtime releases.",
                        "Step 4: Configure `resources.requests` (250m CPU, 256Mi RAM) and `limits` (500m CPU, 512Mi RAM).",
                        "Step 5: Define HTTP `readinessProbe` (determines traffic routing) and `livenessProbe` (triggers container restart on freeze)."
                    ],
                    "code_or_math": "apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: production-api\n  labels:\n    app: backend-api\nspec:\n  replicas: 3\n  strategy:\n    type: RollingUpdate\n    rollingUpdate:\n      maxSurge: 1\n      maxUnavailable: 0\n  selector:\n    matchLabels:\n      app: backend-api\n  template:\n    metadata:\n      labels:\n        app: backend-api\n    spec:\n      containers:\n        - name: api\n          image: myregistry.com/app:v1.2.0\n          ports:\n            - containerPort: 8080\n          resources:\n            requests:\n              cpu: '250m'\n              memory: '256Mi'\n            limits:\n              cpu: '500m'\n              memory: '512Mi'\n          readinessProbe:\n            httpGet:\n              path: /health\n              port: 8080\n            initialDelaySeconds: 5\n            periodSeconds: 10"
                }
            ],
            "practice_questions": [
                {
                    "question": "What is the crucial operational difference between a Kubernetes Liveness Probe and a Readiness Probe?",
                    "options": [
                        "Liveness probe restarts the container when it fails; Readiness probe removes the pod from Service load balancer traffic until it passes",
                        "Readiness probe terminates the underlying Linux EC2 VM; Liveness probe formats disk space",
                        "Liveness probe inspects CPU temperature; Readiness probe monitors git commits",
                        "There is no difference; they are identical aliases"
                    ],
                    "answer": "Liveness probe restarts the container when it fails; Readiness probe removes the pod from Service load balancer traffic until it passes",
                    "explanation": "A Liveness probe detects when an application deadlocks or freezes; if it fails, kubelet kills and restarts the container. A Readiness probe detects whether an app is ready to serve traffic (e.g. warming caches, connecting to DBs); if it fails, the pod remains running but is removed from the Service endpoints to prevent routing traffic to an unready pod."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google & Red Hat",
                    "question": "What happens when a Kubernetes Pod exceeds its configured CPU Limit vs its Memory Limit?",
                    "model_answer": "When a Pod exceeds its CPU Limit, the Linux CFS (Completely Fair Scheduler) throttles the container's CPU shares, causing the application to execute slower, but the process continues running without termination. When a Pod exceeds its Memory Limit, because memory is an inelastic resource, the Linux kernel Out-Of-Memory (OOM) killer immediately terminates the process with exit code 137 (OOMKilled), and kubelet restarts the container.",
                    "interviewer_tip": "Clearly differentiate compressible resources (CPU throttles) from incompressible resources (Memory crashes with OOMKilled 137)."
                }
            ]
        }
    },
    {
        "chapter_num": 5,
        "title": "Infrastructure as Code (IaC) with Terraform: State, Modules & HCL",
        "key_takeaways": "Master HashiCorp Configuration Language (HCL), remote state locking with S3/DynamoDB, modules, and terraform plan/apply lifecycle.",
        "topics": [
            "IaC Paradigms: Declarative (Terraform) vs Imperative (Ansible/Scripts)",
            "Terraform Core Workflow: `init`, `plan`, `apply`, `destroy` & `refresh`",
            "Terraform State (`terraform.tfstate`): Remote backend (S3/GCS) & state locking (DynamoDB) to prevent race conditions",
            "Reusable Terraform Modules: Inputs, outputs, variables, locals, data sources & providers",
            "Terraform Drift Detection, `terraform import` of existing resources & State management commands"
        ],
        "sections": {
            "concept": "Terraform by HashiCorp is the leading open-source declarative Infrastructure as Code tool. Engineers define desired cloud resources in human-readable HashiCorp Configuration Language (HCL). Terraform evaluates dependencies, creates an execution graph, and determines the delta between real-world infrastructure and configuration code during `terraform plan`. The state file (`terraform.tfstate`) maps configuration resources to real-world cloud IDs and attributes. In collaborative enterprise teams, state files must be stored in remote backends (e.g. AWS S3) with distributed state locking (via DynamoDB) to prevent simultaneous applies from corrupting state.",
            "formulas": "1. Terraform Resource Directed Acyclic Graph (DAG): Evaluated concurrently based on dependency tree\n2. Remote State Locking Condition: Apply_Permitted = (Lock_Acquired == True)\n3. Drift Delta: Drift = Actual_Cloud_State - Desired_HCL_State",
            "solved_examples": [
                {
                    "title": "Configuring Secure S3 and DynamoDB Remote Backend in Terraform",
                    "difficulty": "Medium | HashiCorp, AWS, Microsoft",
                    "problem": "Write the Terraform backend configuration block that stores state in an encrypted S3 bucket with DynamoDB state locking.",
                    "step_by_step": [
                        "Step 1: Declare `terraform { backend 's3' { ... } }`.",
                        "Step 2: Specify target S3 bucket and key path (`prod/infrastructure.tfstate`).",
                        "Step 3: Enable server-side encryption with `encrypt = true`.",
                        "Step 4: Specify `dynamodb_table = 'terraform-state-locks'` for distributed locking.",
                        "Step 5: Run `terraform init` to migrate local state to the cloud remote backend."
                    ],
                    "code_or_math": "terraform {\n  required_version = '>= 1.5.0'\n  required_providers {\n    aws = {\n      source  = 'hashicorp/aws'\n      version = '~> 5.0'\n    }\n  }\n  backend 's3' {\n    bucket         = 'enterprise-tfstate-prod'\n    key            = 'network/terraform.tfstate'\n    region         = 'us-east-1'\n    encrypt        = true\n    dynamodb_table = 'terraform-state-lock'\n  }\n}"
                }
            ],
            "practice_questions": [
                {
                    "question": "What happens if two DevOps engineers run `terraform apply` simultaneously on the same project without remote state locking enabled?",
                    "options": [
                        "Terraform automatically merges both applies using git logic",
                        "A race condition occurs that can overwrite, corrupt, or leave the shared `terraform.tfstate` file in an invalid state",
                        "The cloud provider shuts down all running servers",
                        "Terraform converts all resources to JSON"
                    ],
                    "answer": "A race condition occurs that can overwrite, corrupt, or leave the shared `terraform.tfstate` file in an invalid state",
                    "explanation": "Without distributed state locking (such as using AWS DynamoDB with S3 backend), concurrent apply operations trigger race conditions where one engineer's state write overwrites the other, leading to state corruption and orphaned cloud resources."
                }
            ],
            "interview_questions": [
                {
                    "company": "HashiCorp & Cisco",
                    "question": "What is 'Configuration Drift' in Terraform, and how do you detect and fix it?",
                    "model_answer": "Configuration Drift occurs when real-world cloud resources are modified outside of Terraform (e.g. an engineer manually changing security group ports in the AWS console). To detect drift, run `terraform plan` or `terraform refresh`, which queries the live cloud APIs and compares current infrastructure to the Terraform code. To remediate drift, either apply the Terraform configuration to overwrite the out-of-band changes, or update the Terraform code to align with the new desired state.",
                    "interviewer_tip": "Mention `terraform refresh` and immutable infrastructure culture."
                }
            ]
        }
    },
    {
        "chapter_num": 6,
        "title": "Configuration Management & Automated Provisioning with Ansible",
        "key_takeaways": "Master agentless architecture, SSH execution, YAML Playbooks, Inventory files, Roles, and the mathematical principle of Idempotence.",
        "topics": [
            "Ansible Architecture: Agentless push model, SSH transport & Python module execution",
            "Ansible Inventory: Static INI/YAML vs Dynamic Cloud Inventory (AWS EC2 / Azure plugin)",
            "YAML Playbooks: Tasks, Handlers, Variables, Facts & Jinja2 template rendering",
            "Idempotence in depth: Ensuring playbooks can run repeatedly without unintended side effects",
            "Ansible Galaxy, Reusable Roles (tasks, handlers, defaults, vars) & Ansible Vault for secret encryption"
        ],
        "sections": {
            "concept": "Ansible is an open-source automation engine for configuration management, application deployment, and task orchestration. Unlike Chef or Puppet which require background agents installed on target nodes, Ansible is agentless: the control node executes tasks over standard SSH (Linux) or WinRM (Windows) using temporary Python modules. The foundational principle of Ansible is Idempotence: running a playbook once or ten times produces identical system state, only modifying resources that do not match the declared state. Ansible Vault encrypts sensitive variables and credentials using AES-256.",
            "formulas": "1. Idempotence Function: f(f(x)) = f(x) (Applying configuration multiple times yields same system state)\n2. Ansible Task Return: `ok` (already in desired state), `changed` (modified), `failed` (error)\n3. Execution Flow: Control Machine -> SSH -> Python Script Push -> Execute & Gather Facts -> JSON Return -> Delete Script",
            "solved_examples": [
                {
                    "title": "Writing an Idempotent Ansible Playbook to Configure Nginx and SSL Certificates",
                    "difficulty": "Medium | Red Hat, IBM, Rackspace",
                    "problem": "Write a clean Ansible Playbook that installs Nginx, deploys a Jinja2 template configuration, and triggers a service restart only when configuration changes.",
                    "step_by_step": [
                        "Step 1: Define `hosts: webservers` with `become: yes` for sudo privileges.",
                        "Step 2: Task 1: Install Nginx with `state: present` (idempotent: does nothing if already installed).",
                        "Step 3: Task 2: Copy Jinja2 template with `notify: Restart Nginx` handler.",
                        "Step 4: Task 3: Ensure Nginx is enabled and running (`state: started`).",
                        "Step 5: Handlers run at the end of the play only if Task 2 reported `changed: true`."
                    ],
                    "code_or_math": "# Idempotent Ansible Playbook\n- name: Configure Web Fleet\n  hosts: webservers\n  become: yes\n  tasks:\n    - name: Ensure Nginx is installed\n      apt:\n        name: nginx\n        state: present\n        update_cache: yes\n    - name: Deploy Nginx Configuration Template\n      template:\n        src: templates/nginx.conf.j2\n        dest: /etc/nginx/nginx.conf\n      notify: Restart Nginx\n    - name: Ensure Nginx is running\n      service:\n        name: nginx\n        state: started\n        enabled: yes\n  handlers:\n    - name: Restart Nginx\n      service:\n        name: nginx\n        state: restarted"
                }
            ],
            "practice_questions": [
                {
                    "question": "What does it mean for an Ansible playbook task to be 'Idempotent'?",
                    "options": [
                        "It runs faster on Intel processors than AMD processors",
                        "Executing the task multiple times results in the same final system state without making unnecessary changes on repeated runs",
                        "It automatically sends an email to the team lead on completion",
                        "It can only be executed once and is self-deleting"
                    ],
                    "answer": "Executing the task multiple times results in the same final system state without making unnecessary changes on repeated runs",
                    "explanation": "Idempotence means an operation can be applied multiple times without changing the result beyond the initial application. If a package is already installed or a file already contains the desired content, Ansible skips modification and reports `ok` instead of `changed`."
                }
            ],
            "interview_questions": [
                {
                    "company": "Red Hat & IBM",
                    "question": "Why is Ansible's agentless architecture over SSH considered a major advantage over agent-based tools like Puppet or Chef?",
                    "model_answer": "Agent-based systems require installing, managing, updating, and troubleshooting proprietary daemon software on thousands of client nodes, which consumes CPU/RAM and introduces security maintenance overhead. Ansible requires zero client software beyond standard OpenSSH and Python, which exist on virtually every Linux machine by default. This makes onboarding new servers instantaneous and eliminates agent upgrade compatibility issues.",
                    "interviewer_tip": "Highlight reduced attack surface and instant setup time."
                }
            ]
        }
    },
    {
        "chapter_num": 7,
        "title": "Observability, Monitoring, Distributed Tracing & Site Reliability Engineering (SRE)",
        "key_takeaways": "Master the 3 Pillars of Observability (Metrics, Logs, Traces), Prometheus PromQL, Grafana visualization, and SRE error budgets.",
        "topics": [
            "The Three Pillars of Observability: Metrics (Time-series), Logs (Events), Traces (Request journeys)",
            "Prometheus Architecture: Pull model, Exporters (Node Exporter), Time Series Database (TSDB) & Alertmanager",
            "PromQL (Prometheus Query Language): Rates, histograms, percentiles (p95, p99) & alerts",
            "Distributed Tracing: OpenTelemetry, W3C Trace Context, Spans, Jaeger & microservice bottlenecks",
            "SRE Principles: Service Level Indicators (SLI), Service Level Objectives (SLO), and Error Budget burn rate"
        ],
        "sections": {
            "concept": "Observability enables engineers to infer the internal health and failure states of distributed systems based on external telemetry. The Three Pillars are Metrics (numeric time-series aggregated over time), Logs (timestamped textual records of discrete events), and Distributed Tracing (tracking a single user request across hundreds of microservices using unique Trace IDs and Spans). Prometheus pulls metrics from target endpoints over HTTP, storing them in an optimized TSDB. Site Reliability Engineering (SRE), pioneered by Google, aligns product and operations teams using Service Level Objectives (SLOs) and Error Budgets (tolerable downtime used for risky product releases).",
            "formulas": "1. Error Budget % = 100% - SLO% (e.g. 99.9% SLO gives 0.1% error budget = 43.8 minutes downtime/month)\n2. Prometheus 99th Percentile Latency Query: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))\n3. Error Budget Burn Rate: BurnRate = Actual_Error_Rate / Allowed_Error_Rate",
            "solved_examples": [
                {
                    "title": "Calculating SRE Error Budget and Setting up Prometheus PromQL SLO Alert",
                    "difficulty": "Hard | Google, Datadog, Uber",
                    "problem": "Calculate monthly allowed failed requests for an API handling 20,000,000 requests/month with a 99.95% Availability SLO. Write the PromQL query.",
                    "step_by_step": [
                        "Step 1: Error budget percentage = 100% - 99.95% = 0.05% = 0.0005.",
                        "Step 2: Allowed failed requests = 20,000,000 * 0.0005 = 10,000 failed requests allowed per month.",
                        "Step 3: If 8,000 requests fail during a botched deployment, 80% of the monthly error budget is burned, freezing non-essential releases.",
                        "Step 4: Write PromQL query calculating error rate over 5 minutes: `sum(rate(http_requests_total{status=~'5..'}[5m])) / sum(rate(http_requests_total[5m]))`."
                    ],
                    "code_or_math": "# SRE Error Budget Calculation\ntotal_requests = 20_000_000\nslo = 99.95\nerror_budget_pct = (100.0 - slo) / 100.0\nallowed_failures = total_requests * error_budget_pct\nprint(f'Allowed monthly failures: {int(allowed_failures):,} requests')"
                }
            ],
            "practice_questions": [
                {
                    "question": "In Site Reliability Engineering (SRE), what is an 'Error Budget'?",
                    "options": [
                        "The financial budget allocated to buy replacement hard drives",
                        "The amount of downtime or failed requests permitted by a Service Level Objective (SLO), used to balance innovation velocity with reliability",
                        "A list of software bugs found by QA engineers",
                        "The hourly salary of on-call engineers"
                    ],
                    "answer": "The amount of downtime or failed requests permitted by a Service Level Objective (SLO), used to balance innovation velocity with reliability",
                    "explanation": "An Error Budget represents the 100% - SLO margin of acceptable unreliability (e.g. 99.9% SLO allows 0.1% downtime). When the error budget is plentiful, developers can ship high-velocity experimental features; when the budget is depleted, feature releases pause to focus exclusively on stability."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google & Datadog",
                    "question": "Why are p95 and p99 percentiles preferred over Average (Mean) latency when monitoring web application performance?",
                    "model_answer": "Average (mean) latency is heavily skewed and hides severe real-world user degradation. If 98 requests take 10ms and 2 requests take 10,000ms (10 seconds), the average is an acceptable ~210ms, concealing that 2% of users are experiencing catastrophic timeouts. The 99th percentile (p99) accurately reveals the worst-case experience of the slowest 1% of users, which often includes your highest-spending power users making complex queries.",
                    "interviewer_tip": "Connect p99 percentiles to user retention and SLA guarantees."
                }
            ]
        }
    },
    {
        "chapter_num": 8,
        "title": "Solved DevOps SRE Production Outage Scenarios & High-Yield Placement Drills",
        "key_takeaways": "Master diagnosing critical production emergencies: Linux OOM panics, Kubernetes CrashLoopBackOff, SSL certificate expiry, and DNS resolution failures.",
        "topics": [
            "Production Outage 1: Kubernetes Pods stuck in `CrashLoopBackOff` or `ImagePullBackOff`",
            "Production Outage 2: Linux server 100% CPU lockup, zombie processes & high load average troubleshooting",
            "Production Outage 3: Post-mortem analysis of catastrophic DNS resolution failure (CoreDNS failure)",
            "Chaos Engineering: Netflix Chaos Monkey, fault injection & blast radius containment",
            "FAANG DevOps & SRE placement technical interview questions, grading rubrics & live scenario drills"
        ],
        "sections": {
            "concept": "Top tech companies evaluate DevOps candidates through live troubleshooting drills and root-cause analysis (RCA). Systematically diagnose Linux outages starting with resource saturation (USE method: Utilization, Saturation, Errors). If Load Average is high but CPU % is low, processes are waiting in uninterruptible sleep state (D state) on I/O bottlenecks. In Kubernetes, `CrashLoopBackOff` indicates the container starts, throws an unhandled exception or missing configuration file, and exits immediately. Post-mortems must be Blameless: focusing on systemic architectural and procedural fixes rather than human error.",
            "formulas": "1. Linux Load Average: Processes in Running state (R) + Processes in Uninterruptible Disk Sleep (D)\n2. Safe CPU Load Threshold: Load_Average <= Number_of_Physical_CPU_Cores\n3. Kubernetes CrashLoopBackOff Backoff Algorithm: Delay doubles up to 5 minutes: 10s, 20s, 40s, 80s, 160s, 300s",
            "solved_examples": [
                {
                    "title": "Diagnosing and Resolving a Kubernetes `CrashLoopBackOff` Emergency",
                    "difficulty": "Hard | Google, Amazon, Uber",
                    "problem": "A newly deployed production pod is stuck in `CrashLoopBackOff`. Walk through the precise terminal commands to identify the root cause.",
                    "step_by_step": [
                        "Step 1: Check pod status: `kubectl get pods -n production`.",
                        "Step 2: Inspect events and exit codes: `kubectl describe pod <pod-name> -n production`. Look for Last State: Terminated, Reason: Error, Exit Code.",
                        "Step 3: Retrieve stdout/stderr logs from the previous crashed container: `kubectl logs <pod-name> --previous -n production`.",
                        "Step 4: Common findings: Missing environment variable secret (`DATABASE_URL`), failing database connection pool, or missing configmap volume mount.",
                        "Step 5: Apply corrected ConfigMap/Secret and verify pod reaches `Running 1/1` status."
                    ],
                    "code_or_math": "# Kubernetes Rapid Triage Runbook\nkubectl get events --sort-by='.metadata.creationTimestamp' -A\nkubectl logs deployment/api --previous --tail=100"
                }
            ],
            "practice_questions": [
                {
                    "question": "In Linux systems engineering, what does a High Load Average coupled with Low CPU Utilization typically indicate?",
                    "options": [
                        "The motherboard power supply is overheating",
                        "Processes are blocked waiting on slow disk I/O, network storage (NFS), or hardware locks in uninterruptible sleep state (D state)",
                        "A Python script has an infinite loop",
                        "The monitor refresh rate is set to 60Hz"
                    ],
                    "answer": "Processes are blocked waiting on slow disk I/O, network storage (NFS), or hardware locks in uninterruptible sleep state (D state)",
                    "explanation": "Linux load average counts processes actively using CPU plus processes blocked waiting in uninterruptible disk sleep (D state). When CPU is low but load average is high, processes are stalled waiting for disk reads/writes or unresponsive network storage."
                }
            ],
            "interview_questions": [
                {
                    "company": "Google & Meta",
                    "question": "What is a 'Blameless Post-Mortem' in SRE culture, and why is it essential?",
                    "model_answer": "A Blameless Post-Mortem operates on the fundamental assumption that engineers are competent professionals who made the best decisions possible given the information they had at the time. If an engineer pressed a wrong button that took down production, the root cause is not 'human error'\u2014it is why the system permitted a single person to execute a catastrophic action without guardrails, confirmation gates, or automated rollback. Blameless culture encourages transparent reporting of near-misses without fear of punishment, leading to resilient automated safety mechanisms.",
                    "interviewer_tip": "Cite Etsy and Google's SRE book on blameless post-mortems."
                }
            ]
        }
    }
]
