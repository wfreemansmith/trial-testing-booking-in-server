# KSB Master Reference — Wesley Freeman-Smith

## Trial Testing Booking-In Server — L5 Data Engineer EPA

> **Living document** — updated as report, code and conversation develop.
> Three sections: (1) KSB-by-KSB evidence map, (2) Q&A prep, (3) Presentation talking points.
> Assessment Criteria (AC) references map to the AM1 criteria guidance sheet.

---

## SECTION 1 — KSB Evidence Map

### AC1 — K9, S1, S3 | User requirements → scalable, compliant data product

**Distinction:** Justify *why* the product met requirements and served multiple needs — link features to requirements, explain trade-offs, show forward thinking.

| Where | Detail |
| --- | --- |
| **Report** | Scope: "serve multiple users through defined RBAC... scalable, secure solution" |
| **Report** | "Early user requirements gathered from Assessment, Validation and Operations teams, translated to technical specs, refined via testing and research" |
| **Code** | `models/__init__.py` — schema serves multiple user types (centres, examiners, IELTS staff, managers) |
| **Code** | Pydantic schemas enforce consistent data contracts across all user-facing API boundaries |
| **Code** | `User` + `Role` models — three distinct roles (centre_admin, staff, master) map directly to real user groups; each scoped to only what they need |
| **Code** | `get_context` endpoint — returns scoped display_name, centre_id, window_name per user type; frontend hydrated from token, not user-supplied form data |
| **Code** | `api_response()` decorator in `utils/response.py` — consistent JSON envelope `{status, data, message}` across all routes; handles both sync and async functions transparently |
| ⚠️ **Gap** | Add explicit justification: *why* relational DB over alternatives, *why* DAO pattern over raw SQL. Link each to a specific requirement. Mention GDPR compliance via access controls + audit trail |

---

### AC2 — K12, S2 | Business requirements + net-zero / sustainability

| Where | Detail |
| --- | --- |
| **Report** | Scope: "aligns with organisational strategies for sustainable, maintainable systems... contributes to cost efficiency... lowers unnecessary energy use" |
| **Report** | KPIs include time saved, waste reduction (Lean waste types: Waiting, Transportation/Motion, Excess Processing) |
| ⚠️ **Gap** | Mention assessing existing solution's inefficiencies. Reference Docker's resource efficiency vs always-on infrastructure |

---

### AC3 — K7, S27 | Sustainable solutions, ESG, carbon reduction

| Where | Detail |
| --- | --- |
| **Report** | Scope: reusable components, reduced reliance on fragmented on-premises systems |
| **Code** | Normalised DB schema reduces redundant storage; Docker reduces environment overhead |
| ⚠️ **Gap** | Add a sentence on containerisation reducing idle compute. Mention managed cloud with renewable energy as a future step |

---

### AC4 — K13, S4 | Security, scalability, governance in automated pipelines

**Strong evidence — make prominent in report and presentation.**

| Where | Detail |
| --- | --- |
| **Report** | "Role Based and Tokenised Access" — RBAC + token security, least privilege, data protection |
| **Report** | "Validation, error handling" — differentiates user vs system errors; 401 vs 403 distinction (authentication vs authorisation) |
| **Code** | `submit()` — **compensating transaction pattern**: Files.com + PostgreSQL can't share a transaction boundary; `successful_uploads` tracks partial state, rolled back on failure |
| **Code** | `handlers.py` — structured HTTP error responses; generic `HTTPException` handler uses dynamic `e.status_code` so 401/403 handled without duplication; custom exception classes for domain-specific errors |
| **Code** | `models/__init__.py` — FK constraints, `CheckConstraint` on `centre_id` (regex `^[0-9]{4}$`), `nullable=False`, `cascade` delete rules |
| **Code** | `User` model — `token_hash` stores SHA-256 hash only, raw token never persisted; `is_active` for GDPR-aligned soft-disable; `centre_contact_id` FK scopes access to a specific person not just a centre |
| **Code** | `Role` model — `permissions` as PostgreSQL `ARRAY(String)`, `resource:action` convention; `@validates` coerces CSV string with defensive `strip("{ }")` for malformed spacing |
| **Code** | `auth/dependencies.py` — `require_permission()` and `require_centre_permission()` as FastAPI `Depends()` factories; checks token validity (401), window expiry with 7-day grace (403), role permissions (403), centre association (403) |
| **Code** | `dao/auth_dao.py` — `verify_token_get_user()` hashes incoming `?q=` token, queries DB, eager-loads role + centre_contact + marking_window in one round trip |
| **Code** | `get_context` endpoint — `centre_id` and `marking_window_id` derived from trusted user object, not user-supplied form data; eliminates a class of data tampering |
| **Code** | `config.py` — environment-driven config (`development`, `testing`, `production`) loaded from `.env.{ENV}`; `pytest` detection switches env automatically; secrets never hardcoded |
| **Design** | Magic-link pattern: `secrets.token_urlsafe(32)` generates unguessable token; SHA-256 hashed before DB storage; if DB compromised tokens cannot be recovered |
| **Design** | Deliberate bcrypt vs SHA-256 distinction — bcrypt for passwords (slow, salted, brute-force resistant), SHA-256 for random tokens (fast, sufficient given token entropy) |
| **Design** | Dynamic URL-based permission derivation considered and rejected — explicit `resource:action` preferred for clarity, safety, and auditability |
| **Conversation** | K13 + K8 explicitly flagged for compensating transaction / distributed system pattern in `submit()` |

---

### AC5 — S5, B1 | Technical documentation + adapting to changing priorities

| Where | Detail |
| --- | --- |
| **Report** | "Database resourcing" — proactively adapted when Supabase blocked, when AWS SSH lacked tools |
| **Report** | "Testing Approach" — refactored BaseDAO to fix hanging test runner |
| **Code** | Docstrings on every model class, DAO method, service function, and utility |
| **Code** | `README.md` — full environment setup guide: Docker install, env file configuration, `docker-compose up`, access instructions |
| **Code** | `User`, `Role`, `require_permission`, `require_centre_permission`, `verify_token_get_user` — all include docstrings |
| **Code** | `.env.example` and `.env.name.example` — templated config files reduce onboarding friction; documentation of all required env vars |
| ⚠️ **Gap** | Explicitly mention README in report. Note documentation updated as design changed (schema changes, DAO refactor, auth addition) |

---

### AC6 — K6 | Debugging, version control, testing impact on software development

| Where | Detail |
| --- | --- |
| **Report** | "Testing Approach & Version Control" — TDD, Pytest, fixtures, Git, GitHub Actions CI |
| **Report** | Concrete debugging example: BaseDAO `__enter__`/`__exit__` refactor to fix hanging test runner |
| **Code** | `testing/endpoint_tests/test_upload.py` — parametrized tests, async client, 200/400/415/422 coverage; end-to-end submit test covering preview → file_upload → submit flow |
| **Code** | `testing/unit_tests/` — 6 unit test files covering DAOs, utils, controller, file handling, versions |
| **Code** | `testing/conftest.py` — `reset_database` + `setup_database` fixtures ensure test isolation; `cleanup_tmp_files` fixture manages staging directory; async client fixture |
| **Code** | `testing/test_documents/` — 13 test Excel registers covering happy paths, wrong columns, extra columns, totally wrong format |
| **Code** | `logger.py` — Rich handler, INFO/DEBUG level switching based on `--verbose` CLI flag; `config.py` parses `-v` argument; structured logging throughout codebase |
| **Code** | `.github/workflows/docker-testing.yaml` — CI runs on every push; secrets-injected env file; full container build → test → teardown lifecycle; `docker compose run --rm tests` |
| ⚠️ **Gap** | Add cause-and-effect: what did testing *catch*? What did version control *enable*? Don't just describe — show impact. Auth layer still needs 401/403 test coverage |

---

### AC7 — K14 | On-demand cloud computing platforms

| Where | Detail |
| --- | --- |
| **Report** | "Database resourcing" — evaluated Supabase (blocked by Security), AWS SQL Server (lacked dev tools) |
| **Code** | Files.com as managed cloud file storage (PaaS); PostgreSQL via Docker |
| **Code** | `docker-compose.yml` — environment-specific volumes (`pgdata_development`, `pgdata_production`, `pgdata_testing`); clear separation of concerns across environments |
| ⚠️ **Gap (weak KSB)** | Add explicit comparison: Supabase (DBaaS) vs AWS RDS vs Docker PostgreSQL — trade-offs of cost, control, security. Mention IaaS/PaaS/SaaS distinctions. Files.com as PaaS file storage |

---

### AC8 — K8 | Deployment approaches for data pipelines

**Distinction (S16):** Evaluate the success of the algorithm — metrics, accuracy, improvement areas.

| Where | Detail |
| --- | --- |
| **Report** | "Database resourcing" — Docker Compose with dev/test/prod; GitHub Actions CI |
| **Code** | `docker-compose.yml` — three services (db, server, tests), environment-specific volumes, `profiles: ["testing"]` to isolate test runner |
| **Code** | `submit()` — full automated pipeline: retrieve staged files → upload to Files.com → rollback on failure → DB commit |
| **Code** | `.github/workflows/docker-testing.yaml` — automated CI pipeline: checkout → inject secrets → build → test → teardown |
| **Code** | `Dockerfile` — `python:3.12-slim`, creates `tmp_uploads` dir, installs dependencies, sets entrypoint |
| **Conversation** | K8 explicitly noted for `submit()` pipeline orchestration |
| ⚠️ **Distinction gap** | Evaluate `ingest_excel_file()` algorithm: strengths (handles absent markers, prefix stripping, semi-structured input, pandas pipe chain), weaknesses (template-dependent, no OCR). What metrics could you track (processing time, error rate before/after)? |

---

### AC9 — K15 | Star schemas, data lakes, data marts, warehousing

| Where | Detail |
| --- | --- |
| **Scoping doc** | "Potential transformation of data into a star schema for reporting and analytics" |
| ⚠️ **Gap** | Not in report yet. Add to Discussion or Recommendations: current normalised schema is OLTP-optimised; for analytics/Power BI a star schema would be appropriate. Fact table: candidate results. Dims: centre, version, window, examiner, language family |

---

### AC10 — K17, S6 | ETL — clean, validate, combine disparate sources

| Where | Detail |
| --- | --- |
| **Report** | "Extracting and Preparing Seed Data" — integrated SQL Server, Excel, Word docs, text extracts → CSV seed format |
| **Code** | `excel_register_processing.py` — `ingest_excel_file()` uses pandas pipe chain: `rename_columns` → `drop_empty_rows` → `strip_prefixes` → `strip_strings` → `replace_absent_candidates` → `construct_version_ids` → `replace_nans` |
| **Code** | `db/legacy_db_queries/select_centres.sql` — extracts centre data from legacy `Pretesting.dbo.tblCentre` SQL Server table with column aliasing |
| **Code** | `db/legacy_db_queries/select_centre_contacts.sql` — sophisticated CTE + `CROSS APPLY STRING_SPLIT` pattern: unpivots multi-contact columns, splits semicolon-delimited emails, assigns `primary_contact` flag via `ROW_NUMBER()` — real ETL artefact showing legacy data transformation |
| **Code** | `setup_db.py` — walks multiple CSV directories to seed from combined sources |

---

### AC11 — K20 | Data engineering tools in own organisation

| Where | Detail |
| --- | --- |
| **Scoping doc** | Existing tools: PowerBI, SQL Server, Excel |
| **Code** | New stack: FastAPI, SQLAlchemy, Pandas, Pydantic, Pytest, Docker, GitHub Actions, Files.com SDK, Rich (logging), pyodbc (legacy DB connection) |
| **Code** | `pyodbc` + Windows Authentication (`Trusted_Connection`) for legacy SQL Server access — bridges old and new stack |
| ⚠️ **Gap** | Add to report — contrast existing vs new tools with justification. E.g. Pandas over raw SQL for Excel ingestion; SQLAlchemy ORM for modularity and testability; pyodbc as bridge to legacy system |

---

### AC12 — K24, K25, S24 | Evaluate prototypes; solution lifecycle

| Where | Detail |
| --- | --- |
| **Report** | "Database resourcing" — Supabase → Docker lifecycle journey |
| **Report** | "ORM and DAO" — SQL Server vs PostgreSQL; custom UIDs vs integer PKs |
| **Scoping doc** | Full lifecycle: Planning → Design → Development → Consultation → Training → Deployment → Maintenance |
| **Design** | Dynamic URL permission derivation evaluated and rejected — documented design decision with rationale |
| **Code** | Commented-out `@validates` approaches in `Upload`, `Batch`, `Candidate` models — shows iteration; `__init__`-based PK generation chosen deliberately for reliability |
| ⚠️ **Gap** | Make lifecycle explicit in Discussion of Findings. Name strengths AND weaknesses of current prototype state |

---

### AC13 — K26 | Approved organisational architectures and frameworks

| Where | Detail |
| --- | --- |
| **Scoping doc** | "Following the organisation's preference for relational databases" |
| **Code** | `pyodbc` legacy connection maintains compatibility with existing SQL Server infrastructure |
| ⚠️ **Gap** | Add a sentence on aligning with org's SQL Server/PowerBI ecosystem. Mention Agile/sprint delivery if applicable at CUP |

---

### AC14 — K4, S26 | Data quality metrics and frameworks

| Where | Detail |
| --- | --- |
| **Report** | Scope: "ensuring Consistency, Accuracy, Completeness, Timeliness and Validity" |
| **Code** | `excel_register_processing.py` — `validate_candidate()`, `check_for_duplicates()`, `validate_version()`, `check_lists()` |
| **Code** | `check_lists()` — test_date future-date check, version existence check, in-list duplicate detection, global error aggregation |
| **Code** | `models/__init__.py` — DB-level constraints as last-line quality enforcement |
| **Code** | `Role.@validates('permissions')` — defensive `strip("{ }")` guards against malformed CSV input at model level |
| **Code** | `CandidateDAO.is_duplicate_candidate()` — three-case logic: full duplicate (True), number-only duplicate (returns next available number), new candidate (False); uses `itertools.chain` to find max across DB + incoming list |
| ⚠️ **Gap** | Name the DAMA framework explicitly — your five dimensions match it. Shows theoretical grounding |

---

### AC15 — K2, S9 | Query/manipulate data, automated validation, move between systems

| Where | Detail |
| --- | --- |
| **Report** | "Extracting and Preparing Seed Data" — SQL + Pandas + Win32 for legacy extraction |
| **Code** | `base_dao.py` — dynamic SQLAlchemy ORM queries with AND conditions; `select()` and `select_one()` as reusable generic methods |
| **Code** | `upload_dao.py` — `create_upload_object()`: complex nested object creation, version_id lookups via reference dict, batch-candidate assignment |
| **Code** | `candidate_dao.py` — `select_candidates_by_upload()` uses `.like()` pattern matching on composite candidate_id; `is_duplicate_candidate()` cross-references DB state with incoming list |
| **Code** | `submit()` — moves data: temp filesystem → Files.com → PostgreSQL; `model_dump()` converts Pydantic → dict for DAO layer |
| **Code** | `db/legacy_db_queries/` — raw SQL queries for extracting from legacy SQL Server; `select_centre_contacts.sql` uses CTEs, `STRING_SPLIT`, `ROW_NUMBER()`, `UNION ALL` |
| **Code** | `verify_token_get_user()` — SHA-256 hash computed at query time, compared against stored hash; no raw token ever queried |

---

### AC16 — K19, S16 | Structured/semi-structured/unstructured data; extraction algorithms

**Distinction (S16):** Evaluate algorithm success — metrics, strengths, weaknesses, improvements.

| Where | Detail |
| --- | --- |
| **Code** | `excel_register_processing.py` — `ingest_excel_file()` handles semi-structured Excel: user-generated, variable formatting, absent markers, prefix stripping, pandas pipe chain |
| **Code** | `upload_routes.py` — PDF handling (unstructured binary) staged for Files.com |
| **Code** | `db/legacy_db_queries/select_centre_contacts.sql` — extracts from structured SQL Server; handles semi-structured data (semicolon-delimited email field, multiple contact columns) |
| **Report** | "Extracting and Preparing Seed Data" — Word docs, text extracts as unstructured sources |
| ⚠️ **Gap** | Explicitly name the three data types in report. For S16 distinction: evaluate `ingest_excel_file()` — strengths (absent markers, prefix stripping, pipe chain readability), weaknesses (template-dependent, no OCR, `header=4` hardcoded). Reference scoping doc's OCR/CV future suggestion |

---

### AC17 — K30, S23 | Communicating about the data product to different audiences

**Distinction:** Evaluate the *impact* of communication — did it lead to understanding, action, decisions?

| Where | Detail |
| --- | --- |
| **Report** | "Role Based and Tokenised Access" — references K30/S23 |
| **Code** | `README.md` — step-by-step setup guide for technical users; `.env.example` files for onboarding |
| ⚠️ **Gap** | Needs a dedicated section. Describe: ER diagrams for technical stakeholders, workflow diagrams for operational staff, non-technical instructions for centres. For distinction: what *changed* as a result of communication? |

---

### AC18 — S22, B2 | Collaborative working with technical and non-technical stakeholders

| Where | Detail |
| --- | --- |
| **Scoping doc** | "Schedule meetings with Assessment, Validation, Operations and IT teams" |
| ⚠️ **Gap** | Not in report yet — needs a dedicated section. Include: who you met, what was discussed, how feedback shaped decisions (e.g. IT Security blocking Supabase → Docker), how you adapted communication style |

---

## SECTION 2 — Q&A Preparation

### "How did you ensure the data product met user requirements and regulatory compliance?" *(AC1 — K9, S1, S3)*

* Stakeholder interviews → technical specs; requirements refined via testing
* Three roles (centre_admin, staff, master) map to real user groups — each scoped to only what they need
* RBAC + tokenised access for GDPR and data protection
* `get_context` endpoint locks centre_id and marking_window_id to the token — prevents data tampering
* Consistent `api_response()` JSON envelope across all routes — predictable interface for all user types
* Pydantic validation at API boundary; FK constraints + rollbacks for integrity
* **Distinction:** justify *why* — relational DB for referential integrity, DAO for testability

---

### "Describe how sustainable, net-zero technologies were considered" *(AC2/3 — K12, K7, S2, S27)*

* Replacing manual processes reduces Lean waste (Waiting, Motion, Excess Processing)
* Normalised schema reduces storage vs duplicated spreadsheets
* Docker avoids always-on infrastructure; reproducible builds reduce wasted compute
* Future: managed cloud with renewable energy commitments as next step

---

### "How did you incorporate security and scalability into your data pipelines?" *(AC4 — K13, S4)*

* RBAC + magic-link tokens — least privilege, scoped per user type
* Token security: `secrets.token_urlsafe(32)` generates unguessable token; SHA-256 hash stored in DB — raw token never persists; if DB is compromised, tokens cannot be recovered or reused
* Deliberate choice: bcrypt for passwords (slow, salted, brute-force resistant) vs SHA-256 for random tokens (fast, sufficient given token entropy)
* Permissions stored as PostgreSQL ARRAY on Role — `resource:action` convention, checked via FastAPI `Depends()` per route
* 401 vs 403 distinction: 401 = who are you? (token invalid/inactive), 403 = what are you allowed? (wrong role, wrong centre, expired window)
* `is_active` flag allows soft-disabling users without breaking audit trail — GDPR-aligned
* `centre_contact_id` FK scopes a centre user to a specific person, not just a centre
* `config.py` — environment-driven config, no hardcoded secrets; pytest auto-detection switches env automatically
* Dynamic URL permission derivation considered and rejected — explicit `resource:action` preferred for clarity and auditability
* **Compensating transaction pattern in `submit()`** — distributed system integrity; `successful_uploads` rollback on failure
* Docker for scalable, consistent deployment

---

### "How have debugging, version control and testing impacted your development?" *(AC6 — K6)*

* TDD from the start — Pytest unit + endpoint tests, parametrized, async
* 6 unit test files + endpoint tests covering DAOs, utils, file handling, end-to-end submit
* `conftest.py` — `reset_database`/`setup_database` fixtures for full test isolation; `cleanup_tmp_files` manages staging dir
* 13 test Excel registers covering malformed, extra columns, wrong format — tests the algorithm not just the happy path
* Git for version control; GitHub Actions CI — full container build + test + teardown on every push; secrets-injected env
* `logger.py` — Rich handler, `--verbose` CLI flag switches DEBUG/INFO; structured logging throughout enables runtime debugging
* Concrete debugging: SQLAlchemy sessions hanging → refactored BaseDAO context manager
* **Commented-out `@validates` approaches** in models — version history shows deliberate iteration and design decisions

---

### "What deployment approaches did you use and why?" *(AC8 — K8)*

* Docker Compose — dev/test/prod, environment-specific volumes, solved infrastructure blocker
* `profiles: ["testing"]` isolates test runner so it doesn't start in production
* GitHub Actions CI/CD — automated testing on push, secrets-based env injection
* `submit()` orchestrates runtime pipeline: staged files → Files.com → compensating rollback → DB commit
* **Distinction (S16):** `ingest_excel_file()` — pandas pipe chain for readability; handles variable formatting; weakness is `header=4` hardcoded and template dependency

---

### "Describe your ETL method for cleaning and validating data" *(AC10 — K17, S6)*

* `ingest_excel_file()` pipeline: rename → drop empties → strip prefixes → strip strings → replace absents → construct IDs → replace NaNs
* Pydantic as validation layer after Pandas transformation
* `check_lists()` — version validation, duplicate checking, test_date validation, error flagging before DB commit
* Legacy ETL: raw SQL (`select_centres.sql`, `select_centre_contacts.sql`) → CSV seed data from SQL Server
* `select_centre_contacts.sql` — CTE + `CROSS APPLY STRING_SPLIT` unpivots contact columns and splits semicolon-delimited emails; real legacy data transformation artefact

---

### "Which data engineering tools have you found most valuable?" *(AC11 — K20)*

* **Pandas** — flexible semi-structured Excel ingestion; pipe chain for readable transformations
* **SQLAlchemy ORM** — type-safe, modular, cross-engine compatible
* **Pydantic** — validation + clean user-facing error messages; `model_dump()` for clean DAO handoff
* **Docker** — solved infrastructure constraint, reproducible environments
* **FastAPI Depends()** — clean dependency injection for auth without global middleware overhead
* **pyodbc** — legacy SQL Server bridge; Windows Authentication for seamless org integration
* Compared to org's existing tools: SQL Server → PostgreSQL, Excel → structured API

---

### "How do you evaluate prototype strengths and weaknesses?" *(AC12 — K24, K25, S24)*

* Supabase → Docker: identified infrastructure constraint early, adapted
* SQL Server vs PostgreSQL: evaluated Docker compatibility, constraint differences
* Custom UIDs vs integer PKs: deliberate trade-off — human-readable for non-technical staff; commented-out `@validates` approaches show iteration
* Dynamic permission derivation evaluated and rejected — documented design decision
* Test suite as formal evaluation mechanism — 13 test registers, end-to-end submit flow
* Weakness: proof-of-concept, not production-hardened; training and front-end still needed

---

### "What data quality metrics do you track?" *(AC14 — K4, S26)*

* Five dimensions: Consistency, Accuracy, Completeness, Timeliness, Validity (DAMA framework)
* KPIs: time per batch, turnaround, error rate, data accessibility
* `is_duplicate_candidate()` — three-case duplicate logic including auto-renumbering
* Validation flags in API response — user-correctable before commit
* DB constraints as last-line enforcement
* Model-level `@validates` guards malformed input before it reaches the DB

---

### "How do you tailor communication to different audiences?" *(AC17 — K30, S23)*

* ER diagrams → technical stakeholders; workflow diagrams → operational staff
* README + `.env.example` files → developers; non-technical work instructions → centre users
* `api_response()` envelope provides consistent, human-readable status/message for frontend consumption
* **Distinction:** reflect on impact — did communication lead to a decision or requirement change?

---

### "Describe a collaborative project with different stakeholders" *(AC18 — S22, B2)*

* Requirements gathering: Assessment, Validation, Operations, IT/Security
* IT/Security constraint directly shaped Docker architecture decision
* Schema design informed by operational team workflows
* Adapted communication style: technical detail for IT, process-level for operational teams

---

## SECTION 3 — Presentation Talking Points

| Slide | Key points | KSBs |
| --- | --- | --- |
| **Problem & Business Case** | Manual spreadsheets → integrity risks, no audit trail. KPIs quantify business case | S1, S2, K9 |
| **Solution Architecture** | Three-tier system. ER diagram. Normalised schema, RBAC, multi-user. api_response envelope | S3, K13, K9 |
| **ETL Pipeline** | Excel → Pandas pipe chain → Pydantic → DAO → DB. Legacy SQL ETL (CTE/STRING_SPLIT). Error handling flow | K17, S6, K2, S9 |
| **Security & Governance** | RBAC + magic-link tokens. SHA-256 rationale. Role permissions array. 401/403 distinction. Compensating transaction in `submit()` | K13, S4 |
| **Deployment & Testing** | Docker Compose (dev/test/prod). GitHub Actions CI. TDD Pytest (6 unit + endpoint). Rich logging + verbose mode | K6, K8, B1 |
| **Sustainability & Alignment** | Lean waste reduction. Reusable components. pyodbc legacy bridge. Org ecosystem alignment | K7, K12, S27, K26 |
| **Evaluation & Future** | Prototype decisions. Design alternatives considered. Commented iterations. Path to production. Star schema, front-end, OCR roadmap | K24, K25, K15, S24 |

---

## GAPS SUMMARY — Prioritised Report Actions

| Priority | AC | KSB | Action |
| --- | --- | --- | --- |
| 🔴 High | AC18 | S22, B2 | Add collaborative working section — who, discussions, how feedback shaped decisions |
| 🔴 High | AC17 | K30, S23 | Add communication section + distinction reflection on impact |
| 🔴 High | AC9 | K15 | Add star schema paragraph in Discussion/Recommendations |
| 🟡 Medium | AC7 | K14 | Cloud platform comparison — Supabase vs AWS vs Docker, IaaS/PaaS/SaaS |
| 🟡 Medium | AC11 | K20 | Contrast existing vs new tools with justification; mention pyodbc legacy bridge |
| 🟡 Medium | AC13 | K26 | Add sentence on aligning with org's SQL Server/PowerBI ecosystem |
| 🟡 Medium | AC12 | K25 | Make lifecycle explicit in Discussion of Findings; reference commented-out iterations |
| 🟢 Low | AC5 | S5 | Mention README and `.env.example` files explicitly in report |
| 🟢 Low | AC16 | K19 | Name structured/semi-structured/unstructured types in report; mention `select_centre_contacts.sql` as semi-structured legacy extraction |
| 🟢 Low | AC8/16 | S16 | Evaluate `ingest_excel_file()` algorithm for distinction; note `header=4` as a weakness |
| 🟢 Low | AC14 | K4 | Name DAMA framework explicitly; mention `is_duplicate_candidate()` three-case logic |
| 🟢 Low | AC6 | K6 | Add cause-and-effect examples: what testing *caught*, what CI *prevented* |

---

## STILL TO BUILD — Auth Implementation Tracker

| Item | Status |
| --- | --- |
| `User` model (token_hash, role_id, centre_contact_id FK nullable, is_active, hybrid_property display_name) | ✅ Done |
| `Role` model (role_name, ARRAY(String) permissions, @validates with isinstance guard + strip("{ }")) | ✅ Done |
| `User.@validates('token_hash')` — SHA-256 hash on assignment, 64-char passthrough guard | ⚠️ Bug — `@validates` missing field name argument, needs `@validates('token_hash')` |
| `db/data/8.roles.csv` seed file (static) | ✅ Done |
| `db/dummy_data/8.users.csv` seed file (plaintext tokens, hashed by seeder) | ✅ Done |
| `get_db()` generator function for FastAPI Depends() | ✅ Done |
| `verify_token_get_user()` in `dao/auth_dao.py` | ⚠️ In `auth/dependencies.py` for now — consider moving to `dao/auth_dao.py` |
| `require_permission()` in `auth/dependencies.py` | ✅ Done |
| `require_centre_permission()` — as above + centre_contact None guard | ✅ Done |
| `get_context` endpoint — hydrates frontend with scoped user data | ✅ Done |
| All upload routes wired with appropriate Depends() | ✅ Done |
| `UploadPayload` cleaned up (token field removed) | ✅ Done |
| `UploadFileData` cleaned up (centre_id/marking_window_id removed) | ✅ Done |
| `parse_pg_array()` utility in seeder | ⏳ To do |
| Token generation + SHA-256 hashing in seeder (`secrets` + `hashlib`) | ⏳ To do |
| 401/403 tests added to test suite | ⏳ To do |
| `joinedload(User.centre_contact).joinedload(CentreContact.centre)` — fix joinedload syntax (currently passing class not relationship) | ⚠️ Minor bug to fix |

---

*Last updated: full codebase review from uploaded zip. New evidence added: legacy SQL ETL queries (CTE/STRING_SPLIT), GitHub Actions workflow detail, config.py env switching + pytest detection, logger.py Rich handler + verbose mode, api_response() decorator, is_duplicate_candidate() three-case logic, conftest.py test isolation fixtures, 13 test register files, commented-out model iterations as prototype evidence, pyodbc legacy bridge.*
