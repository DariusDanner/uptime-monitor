# uptime-monitor

A small self-hosted uptime monitor. It checks a list of URLs on a schedule, 
stores each result and serves a status page showing current state and recent history.

The application is deliberately simple. The point of this project is the
infrastructure around it.

##Status

In progress. Currently at Phase 0 of 7 -repo setup.

##Planned stack

-Application: API + background checker + PostgreSQL
-Containers: Docker, multi-stage builds
-Orchestration: K8s (kind locally, AKS in Azure)
-Packaging: Helm 
-IaC: Terrafarm, remote state in Azure Storage 
-CI/CD: GitHub Actions with OIDC federated credentials 

##Repository layout

| Path | Contents |
| `app/` | Application source and Dockerfile |
| `infra/` | Terraform configuration |
| `charts/` | Helm chart |
| `docs/` | Architecture notes and roadmap |

##Running it

Not yet runnable.
