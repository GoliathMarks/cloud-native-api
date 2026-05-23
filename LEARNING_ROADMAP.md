# Cloud-Native & AI/ML Learning Roadmap

**Format:** Project-based — every phase builds directly on the `cloud-native-api` repo  
**Pace:** 7–10 hours/week · ~20 weeks total  
**Starting point:** You already know Docker, Kubernetes basics, Terraform, AWS, Python, and CI/CD. This roadmap deepens and modernizes that foundation.

---

## The Arc

Each phase ships a real, working feature to the same codebase. By the end you'll have a production-grade, AI-powered REST API running on Kubernetes, provisioned entirely with Terraform, and deployed via automated CI/CD.

```
Phase 1 → Production-ready FastAPI app with a real database, auth, and metrics endpoint
Phase 2 → All infrastructure provisioned with Terraform on AWS
Phase 3 → App on Kubernetes with Helm, HPA, probes, and full Prometheus/Grafana observability
Phase 4 → AI-powered features: LLM integration, embeddings, RAG pipeline
Phase 5 → Geospatial optimization service: async TSP solver with GIS data on EKS, Kubernetes Jobs, and KEDA autoscaling
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
- **Prometheus metrics endpoint** (`/metrics`) using `prometheus-fastapi-instrumentator`
  - Automatic instrumentation: request count, latency histograms, error rates per endpoint
  - Custom business metric: items created per minute
- Deploy to **Fly.io** (free tier, dead-simple first cloud deploy)

### Key concepts
- Async Python patterns (`async`/`await`, async context managers)
- 12-factor app methodology
- Database migration workflows
- Stateless authentication with JWTs
- The difference between dev/staging/prod config management
- The four golden signals: latency, traffic, errors, saturation

### Resources
- FastAPI docs: SQL (Relational) Databases — https://fastapi.tiangolo.com/tutorial/sql-databases/
- SQLAlchemy 2.0 async docs — https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- Alembic tutorial — https://alembic.sqlalchemy.org/en/latest/tutorial.html
- Fly.io quickstart — https://fly.io/docs/languages-and-frameworks/python/
- prometheus-fastapi-instrumentator — https://github.com/trallnag/prometheus-fastapi-instrumentator

### Milestone
`git push` triggers CI, builds a Docker image, and deploys a live URL on Fly.io with a real database behind it. `curl /metrics` returns Prometheus-formatted latency and request count data for every endpoint.

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

## Phase 3: Kubernetes & Observability
**Weeks 7–11 · ~40 hours**  
**Goal:** Run the app on Kubernetes and instrument the entire stack with Prometheus and Grafana.

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

**Observability stack (Week 11)**
- Install **kube-prometheus-stack** via Helm — one chart that deploys:
  - **Prometheus** + Prometheus Operator (scrapes all targets automatically)
  - **Grafana** (pre-wired to Prometheus)
  - **Alertmanager**
  - Node Exporter (host-level CPU, memory, disk, network)
  - kube-state-metrics (pod restarts, deployment status, resource utilization)
- Add a `ServiceMonitor` to your app's Helm chart so Prometheus auto-discovers and scrapes your `/metrics` endpoint
- Build a **Grafana dashboard** covering:
  - Request rate, error rate, and p50/p95/p99 latency (from your app's `/metrics`)
  - Pod CPU and memory utilization
  - HPA scaling events
  - PostgreSQL connection pool depth
- Write **Alertmanager rules**:
  - Alert when error rate exceeds 1% over 5 minutes
  - Alert when p99 latency exceeds 500ms
  - Alert when a pod has restarted more than 3 times in an hour
- Expose Grafana through your Ingress at `/grafana`

### Key concepts
- The difference between Deployments, ReplicaSets, and Pods
- Why readiness vs. liveness probes matter in production
- Helm templating and chart structure
- How HPA works and how to test it
- Namespaces and RBAC basics
- The Prometheus data model: metrics, labels, and the scrape loop
- PromQL basics: `rate()`, `histogram_quantile()`, `increase()`
- Push vs. pull monitoring — why Prometheus uses pull
- The difference between infrastructure metrics, app metrics, and business metrics
- Alerting philosophy: alert on symptoms (user impact), not causes

### Resources
- Kubernetes docs: https://kubernetes.io/docs/home/
- kind quickstart — https://kind.sigs.k8s.io/docs/user/quick-start/
- Helm docs — https://helm.sh/docs/
- EKS workshop — https://www.eksworkshop.com/
- kube-prometheus-stack chart — https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack
- Prometheus docs — https://prometheus.io/docs/introduction/overview/
- PromQL cheat sheet — https://promlabs.com/promql-cheat-sheet/
- Grafana dashboard best practices — https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/

### Milestone
`helm upgrade --install cloud-native-api ./helm` deploys a new version to EKS. The HPA scales the deployment under load. Grafana shows live request latency and error rates. An Alertmanager rule fires when the error rate spikes — you see it in the dashboard before you'd notice it in the logs.

---

## Phase 4: AI/ML Engineering
**Weeks 12–15 · ~35 hours**  
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

## Phase 5: Geospatial Optimization Service — TSP on Kubernetes
**Weeks 16–20 · ~40 hours**  
**Goal:** Build an async optimization API that accepts GIS waypoints, solves the Traveling Salesman Problem, and runs the heavy computation as a Kubernetes Job on EKS — a realistic pattern for any CPU-intensive workload.

### What you'll build

**Part A — Async Job API (Week 16)**
- New router at `/tsp` with four endpoints:
  - `POST /tsp/jobs` — submit a TSP problem; returns a `job_id` immediately (202 Accepted)
  - `GET /tsp/jobs/{job_id}` — poll status (`queued` / `running` / `completed` / `failed`)
  - `GET /tsp/jobs/{job_id}/result` — fetch the optimized route as a GeoJSON `LineString`
  - `DELETE /tsp/jobs/{job_id}` — cancel a queued or running job
- Request body accepts:
  - `waypoints`: a GeoJSON `FeatureCollection` of `Point` features (each with an optional `name` property)
  - `algorithm`: `"or_tools"` | `"two_opt"` | `"nearest_neighbor"` (default: `"or_tools"`)
  - `distance_type`: `"haversine"` (great-circle) | `"road_network"` (real road distances via OSRM)
  - `time_limit_seconds`: solver time budget (default: 30)
  - `return_geometry`: if true, response includes the full route `LineString`; if false, just the ordered stop list
- Pydantic models for `TSPJobRequest`, `TSPJobStatus`, and `TSPJobResult`
- Store job state in **Redis** (fast, ephemeral — results don't need to outlive the session)

**Part B — TSP Solver Worker (Week 17)**
- Implement the solver as a standalone Python module (`app/solver/tsp.py`) so it can run anywhere
- **OR-Tools** (`ortools.constraint_solver`) for the primary solver — Google's production-grade routing library
- **2-opt** local search as a fallback / educational reference implementation
- Haversine distance matrix computed with `shapely` + `pyproj`; road-network distances fetched from a self-hosted **OSRM** container
- Unit-test the solver independently of FastAPI — distance matrix correctness, known small-instance optimal solutions
- Containerize the worker separately from the API (`Dockerfile.worker`)

**Part C — Kubernetes Jobs for Compute Workloads (Week 18)**
- When a TSP job is submitted, the API enqueues it to **Redis Streams**
- A **Kubernetes Job** (not a Deployment) is launched per solve request — runs to completion, then exits
- Learn when to use `Job` vs `Deployment` vs `CronJob`:
  - `Deployment`: long-running servers
  - `Job`: run-to-completion compute tasks
  - `CronJob`: scheduled recurring tasks
- Add the solver `Job` manifest to your Helm chart with `ttlSecondsAfterFinished` for automatic cleanup
- Worker reads from Redis Streams, solves, writes result back, marks job complete
- Add **KEDA** (Kubernetes Event-Driven Autoscaling) to scale solver worker replicas based on Redis Stream consumer lag — zero workers at idle, scales up instantly under load

**Part D — OSRM Road Network (Week 19)**
- Run **OSRM** (Open Source Routing Machine) as a sidecar service in your cluster
- Download an OpenStreetMap `.pbf` extract for your target region (e.g., US Northeast from Geofabrik)
- Pre-process the road graph with `osrm-extract` + `osrm-partition` + `osrm-customize` in a Kubernetes `Job`
- Use OSRM's Table API to fetch real driving-distance matrices between waypoints
- Compare haversine vs. road-network results on the same waypoint set — see where straight-line distance misleads the solver

**Part E — End-to-End Integration & Observability (Week 20)**
- Add Prometheus metrics specific to the TSP service:
  - `tsp_jobs_submitted_total` (counter)
  - `tsp_solve_duration_seconds` (histogram, labeled by `algorithm` and `distance_type`)
  - `tsp_queue_depth` (gauge, from Redis Stream pending count)
  - `tsp_job_result_waypoints` (histogram — distribution of problem sizes)
- Extend your Grafana dashboard: job throughput, solver latency by algorithm, queue depth vs. worker count
- Write an end-to-end integration test: submit a 10-city job, poll until complete, assert the result visits every city exactly once
- Load test with `locust`: 50 concurrent job submissions; watch KEDA scale workers and Grafana show queue drain

### Key concepts
- **Async job pattern**: why long-running compute must be decoupled from the HTTP request/response cycle
- **Redis Streams** vs. queues vs. pub/sub — when to use each
- **Kubernetes Jobs**: run-to-completion semantics, `backoffLimit`, `ttlSecondsAfterFinished`, pod restart policies
- **KEDA**: event-driven autoscaling tied to external metrics (queue depth) rather than CPU
- **GeoJSON**: the standard format for geospatial data interchange — `FeatureCollection`, `Feature`, `Point`, `LineString`
- **Haversine formula**: computing great-circle distance between lat/lng coordinates
- **TSP fundamentals**: NP-hard problem class, why exact solvers only scale to ~20 nodes, why heuristics dominate in practice
- **OR-Tools routing**: how Google's solver encodes TSP as a vehicle routing problem (VRP) with one vehicle
- **2-opt local search**: understand the algorithm you're replacing so you know what OR-Tools is doing better
- **OSRM internals**: Contraction Hierarchies preprocessing, why querying a pre-processed graph is microseconds not seconds
- Separating **compute workers** from **API servers** as distinct Deployments with distinct resource profiles

### Resources
- OR-Tools Vehicle Routing — https://developers.google.com/optimization/routing/tsp
- GeoJSON spec (RFC 7946) — https://datatracker.ietf.org/doc/html/rfc7946
- Shapely docs — https://shapely.readthedocs.io/
- pyproj (coordinate transforms) — https://pyproj4.github.io/pyproj/
- OSRM API docs — https://project-osrm.org/docs/v5.24.0/api/
- Geofabrik OSM extracts — https://download.geofabrik.de/
- Redis Streams intro — https://redis.io/docs/latest/develop/data-types/streams/
- KEDA docs — https://keda.sh/docs/
- KEDA Redis Streams scaler — https://keda.sh/docs/scalers/redis-streams/
- Kubernetes Jobs docs — https://kubernetes.io/docs/concepts/workloads/controllers/job/
- Locust load testing — https://locust.io/

### Milestone
`POST /tsp/jobs` with a 25-city GeoJSON payload returns a `job_id` in under 50ms. Polling `/tsp/jobs/{job_id}` transitions from `queued` → `running` → `completed`. The result is a valid GeoJSON `LineString` visiting all 25 cities exactly once. Grafana shows solver latency, queue depth, and KEDA scaling the worker fleet from 0 → N → 0 as the batch drains. The OSRM road-network solve produces a measurably shorter real-world route than the haversine solve on the same inputs.

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
| Monitoring | Prometheus at Raytheon | kube-prometheus-stack, PromQL, Grafana dashboards, Alertmanager |
| AI/ML | Adjacent (swarm, SLAM, robotics) | LLM APIs, embeddings, RAG, MLflow |
| GIS / Geospatial | SLAM, sensor fusion | GeoJSON, haversine, OSRM road-network routing |
| Combinatorial optimization | Robotics path planning | TSP, OR-Tools VRP solver, 2-opt local search |
| Async job queues | — | Redis Streams, Kubernetes Jobs, KEDA event-driven autoscaling |
