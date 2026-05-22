# Cloud-Native & AI/ML Learning Roadmap

**Format:** Project-based — every phase builds directly on the `cloud-native-api` repo  
**Pace:** 7–10 hours/week · ~14 weeks total  
**Starting point:** You already know Docker, Kubernetes basics, Terraform, AWS, Python, and CI/CD. This roadmap deepens and modernizes that foundation.

---

## The Arc

Each phase ships a real, working feature to the same codebase. By the end you'll have a production-grade, AI-powered REST API running on Kubernetes, provisioned entirely with Terraform, and deployed via automated CI/CD.

```
Phase 1 → Production-ready FastAPI app with a real database and auth
Phase 2 → All infrastructure provisioned with Terraform on AWS
Phase 3 → App running on Kubernetes with Helm, HPA, and probes
Phase 4 → AI-powered features: LLM integration, embeddings, RAG pipeline
```

---

## Phase 1: Production-Ready Cloud-Native API
**Weeks 1–3 · ~25 hours**  
**Goal:** Take the scaffold and make it something you'd actually deploy.

### What you'll build
- Swap the in-memory store for a real **PostgreSQL** database
- Async database access with **SQLAlchemy 2.0** + **asyncpg**
- Schema migrations with **Alembic**
- **JWT authentication** (register, login, protected routes)
- Environment-based config with **Pydantic Settings** (12-factor)
- Structured JSON logging
- API versioning (`/v1/items`)
- Deploy to **Fly.io** (free tier, dead-simple first cloud deploy)

### Key concepts
- Async Python patterns (`async`/`await`, async context managers)
- 12-factor app methodology
- Database migration workflows
- Stateless authentication with JWTs
- The difference between dev/staging/prod config management

### Resources
- FastAPI docs: SQL (Relational) Databases — https://fastapi.tiangolo.com/tutorial/sql-databases/
- SQLAlchemy 2.0 async docs — https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- Alembic tutorial — https://alembic.sqlalchemy.org/en/latest/tutorial.html
- Fly.io quickstart — https://fly.io/docs/languages-and-frameworks/python/

### Milestone
`git push` triggers CI, builds a Docker image, and deploys a live URL on Fly.io with a real database behind it.

---

## Phase 2: Infrastructure as Code
**Weeks 4–6 · ~25 hours**  
**Goal:** Provision everything with Terraform — no clicking in the AWS console.

### What you'll build
- **Terraform** project that provisions the full AWS stack:
  - VPC, subnets, security groups
  - **RDS PostgreSQL** (managed database)
  - **ECR** repository for Docker images
  - **ECS Fargate** service running your API
  - **ALB** (Application Load Balancer) in front of it
- Remote Terraform state in **S3 + DynamoDB**
- Terraform modules for reusable components
- Update the **GitHub Actions CI/CD** to build → push to ECR → deploy to ECS on every merge to `main`

### Key concepts
- Terraform state management and remote backends
- Writing reusable Terraform modules
- IAM roles and least-privilege security
- The difference between `terraform plan` and `terraform apply`
- Immutable infrastructure: redeploy don't patch

### Resources
- Terraform AWS provider docs — https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- Terraform: Up & Running (book by Yevgeniy Brikman) — best Terraform learning resource available
- AWS ECS Fargate with Terraform — search "terraform ecs fargate tutorial"

### Milestone
`terraform apply` from a cold AWS account provisions the entire stack in under 10 minutes. A `git push` to `main` deploys a new version automatically.

---

## Phase 3: Kubernetes
**Weeks 7–10 · ~30 hours**  
**Goal:** Run the app on Kubernetes — locally first, then on EKS.

### What you'll build
- Local k8s cluster with **kind** (Kubernetes in Docker)
- Full set of **Kubernetes manifests**:
  - `Deployment` with rolling updates
  - `Service` + `Ingress`
  - `ConfigMap` and `Secret` for environment config
  - **Liveness and readiness probes** wired to your `/health` endpoint
  - Resource `requests` and `limits`
- Convert manifests to a **Helm chart** with templated values
- **Horizontal Pod Autoscaler** (HPA) based on CPU
- Migrate the Terraform stack from ECS → **EKS** (Elastic Kubernetes Service)
- Update CI/CD to `helm upgrade --install` on deploy

### Key concepts
- The difference between Deployments, ReplicaSets, and Pods
- Why readiness vs. liveness probes matter in production
- Helm templating and chart structure
- How HPA works and how to test it
- Namespaces and RBAC basics

### Resources
- Kubernetes docs: https://kubernetes.io/docs/home/
- kind quickstart — https://kind.sigs.k8s.io/docs/user/quick-start/
- Helm docs — https://helm.sh/docs/
- EKS workshop — https://www.eksworkshop.com/

### Milestone
`helm upgrade --install cloud-native-api ./helm` deploys a new version to EKS. The HPA scales the deployment under load. The `/health` endpoint gates traffic during rollouts.

---

## Phase 4: AI/ML Engineering
**Weeks 11–14 · ~35 hours**  
**Goal:** Add AI-powered features and build your first ML pipeline.

### What you'll build

**Part A — LLM Integration (Week 11)**
- Add an endpoint that uses the **Anthropic API** to auto-generate item descriptions
- Use **structured outputs** (tool use) to extract and validate structured data from LLM responses
- Rate limiting and cost controls for API calls

**Part B — Semantic Search with Embeddings (Week 12)**
- Add a **vector database** (**Qdrant** — easy to run in Docker)
- Embed item descriptions using the Anthropic or OpenAI embeddings API
- New endpoint: `GET /items/search?q=something` does semantic similarity search
- Keep the vector store in sync with PostgreSQL

**Part C — RAG Pipeline (Week 13)**
- Build a **Retrieval-Augmented Generation** endpoint:
  `POST /ask` — accepts a natural language question, retrieves relevant items, answers using Claude
- Learn chunking, retrieval strategies, and prompt construction

**Part D — ML Model Serving (Week 14)**
- Train a simple **scikit-learn** classifier (e.g., categorize items by description)
- Track experiments with **MLflow**
- Serve the model as a FastAPI endpoint (`POST /items/classify`)
- Containerize the model server separately — your first ML microservice

### Key concepts
- LLM API patterns: streaming, tool use, structured outputs
- Embeddings and vector similarity search
- RAG architecture and chunking strategies
- The difference between ML training and inference environments
- MLflow experiment tracking and model registry

### Resources
- Anthropic API docs — https://docs.anthropic.com
- Qdrant quickstart — https://qdrant.tech/documentation/quickstart/
- MLflow docs — https://mlflow.org/docs/latest/index.html
- Anthropic cookbook (practical examples) — https://github.com/anthropics/anthropic-cookbook

### Milestone
A single API with four distinct AI capabilities: LLM-generated content, semantic search, natural language Q&A, and ML-based classification — all running on Kubernetes, all provisioned with Terraform.

---

## Suggested Weekly Rhythm

| Day | Activity |
|-----|----------|
| Mon/Tue | Read docs + watch any relevant videos (~2 hrs) |
| Wed/Thu | Build the week's feature with Claude helping (~4 hrs) |
| Fri/Sat | Write tests, clean up, commit + push (~2 hrs) |

---

## How to Use Claude While Learning

The most effective pattern is **explain then do**:

1. Before building something new: *"Explain how Alembic migrations work before we write any code"*
2. While building: *"Write the SQLAlchemy model for Item, then explain each part"*
3. When stuck: paste the error and ask *"What's causing this and why?"*
4. After building: *"Review what we just wrote — what would a senior engineer change?"*

Building the real thing is the point. Reading without doing won't stick.

---

## Quick Reference: What You Already Know vs. What's New

| Topic | Your Foundation | What's New Here |
|-------|----------------|-----------------|
| Docker | Strong | Multi-stage builds, health checks ✅ done |
| Python | Expert | Async patterns, Pydantic v2, modern FastAPI |
| Kubernetes | Familiar | Helm, HPA, probes, EKS, production patterns |
| Terraform | Solid | Modules, remote state, ECS→EKS, full stack |
| CI/CD | Strong (GitLab/Jenkins) | GitHub Actions, ECR push, Helm deploy |
| AWS | Solid | RDS, ECS Fargate, EKS, ALB, ECR together |
| AI/ML | Adjacent (swarm, SLAM, robotics) | LLM APIs, embeddings, RAG, MLflow |
