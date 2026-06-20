1st week:

Get base infra with docker compose, CI/CD
Related structure and unstructured data curation
Abstract class and product setup deploy
Commutation test
Data seeding
Traffic should flow from UI -> Backend -> Engine -> Other dependencies.
Dev tooling

2nd week:

Basic NL2SQL with Vanna
DQ agent
* Suggest relationships
* Suggest naming
* Suggest modelling
* Suggest semantic enrichment
* Data type optimisation
* DDL enrichment
Note: To show real value of this, we need to curate this dataset.
Ingestion pipeline
Backend baseline

3rd week:

Agentic orchestration
Check pointer configuration
Cache configuration

4th week:

Prompt turing
Observability
Integration with backend and UI

5th week:

Prompt turing
Integration with backend and UI
Testing
Sales pitch
Cost modelling


---

Stack:

Docker compose (Self Hosted)
* Traefik/Nginx
* Engine
* Backend
* UI
* LiteLLM
* LangFuse
* MS SQL
* Postgres
* Redis
* Mem0

Communication: REST

----

Immediate next steps:

* Entity High cardinality manager
* Okta configuration if needed
* Building scalable solution
* AuthN and AuthZ - multi-org (paas/saas offering rollout)
* Cloud infra
* Move away from REST to streaming or streaming + pub-sub