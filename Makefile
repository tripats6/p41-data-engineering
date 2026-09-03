PYTHON := python
DBT := dbt
MONTHS := 202501 202502 202503

.PHONY: pipeline ingest dbt-run dbt-test

pipeline: ingest dbt-run dbt-test

ingest:
	$(PYTHON) -m ingestion.ingest --months $(MONTHS)

dbt-run:
	$(DBT) run --project-dir dbt --profiles-dir dbt

dbt-test:
	$(DBT) test --project-dir dbt --profiles-dir dbt
