# AI Usage

AI assistance was used during development of this project as a coding and review aid.

## Areas Where AI Assisted

AI was used to help with:

- Structuring the Python ingestion workflow.
- Drafting and reviewing DuckDB ingestion logic.
- Developing dbt staging, dimension, fact, and mart models.
- Suggesting data-quality tests and SQL validation queries.
- Reviewing modeling decisions around historical station IDs and the current GBFS station snapshot.
- Drafting analytical SQL queries and organizing findings.
- Reviewing project documentation and reproducibility requirements.

## Engineering Decisions

AI-generated suggestions were reviewed and tested locally rather than being accepted blindly.

In particular, the station relationship between historical trip station IDs and the current GBFS station IDs was tested. The identifiers had no direct overlap, so the proposed foreign-key relationship was removed rather than forcing an incorrect mapping.

The same approach was applied to historical station names. Because station IDs can have multiple historical names and the current GBFS data represents a live snapshot, the pipeline preserves the historical trip station information rather than silently applying an approximate mapping.

## Validation

The implementation was validated by running:

- Python ingestion unit tests.
- dbt model builds.
- dbt data-quality tests.
- Custom dbt business-rule tests.
- Composite-grain uniqueness tests for analytical marts.
- The complete `make pipeline` workflow.

The final pipeline successfully completed ingestion, all 8 dbt models, and all 56 dbt tests.
