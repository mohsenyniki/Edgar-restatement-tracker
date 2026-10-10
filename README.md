# EDGAR Restatement Tracker

A daily pipeline that detects when US public companies revise financial numbers they already reported to the SEC, measures how much changed, and classifies each revision as an error or benign.

> **Status:** 🚧 Early development. Repo structure in place; pipeline in progress.

## Why
Every 10-Q and 10-K repeats figures from earlier periods. When those figures quietly change between filings, it can signal an accounting error, or just a benign change like a reclassification or stock split. This project tracks those changes using real SEC EDGAR data.

## How it will work
1. **Ingest:** pull company financial data from SEC EDGAR on a daily schedule
2. **Compare:** match each reported figure against earlier reports for the same period
3. **Flag & classify:** record what changed, by how much, and whether it looks like an error or benign
4. **Serve:** dashboard with a watchlist, company pages, and a restatement alerts feed

## Planned stack
Python · Airflow · dbt · SQL warehouse · AWS (kept to a few dollars/month)

## Repo layout
| Folder | Purpose |
|---|---|
| `ingestion/` | EDGAR data pulls |
| `airflow/` | DAGs for scheduling |
| `dbt/`, `warehouse/` | Models and warehouse setup |
| `dashboard/` | Front end |
| `infra/` | Infrastructure config |
| `notebooks/` | Data exploration |
| `tests/` | Tests |
| `docs/` | Notes and design decisions |

## Roadmap
- [x] Repo structure
- [ ] EDGAR ingestion
- [ ] Restatement detection logic
- [ ] Error vs. benign classification
- [ ] Scheduled Airflow runs
- [ ] Dashboard

Setup instructions will be added once the pipeline runs end to end.
