# KSB Master Reference — Wesley Freeman-Smith

## Trial Testing Booking-In Server — L5 Data Engineer EPA

> **Living document** — updated as report, code and conversation develop.
> Three sections: (1) KSB-by-KSB evidence map, (2) Q&A prep, (3) Presentation talking points.
> Companion document: `EPA_Interview_Prep.md` — revision notes for the assessor Q&A session.

---

## REPORT STATUS OVERVIEW

| Section | Status |
| --- | --- |
| Executive Summary | ⏳ Not yet written |
| Introduction | ✅ Written |
| Scope (KPIs, aims, objectives) | ✅ Written |
| Project Plan | ⏳ Placeholder — needs process diagrams, timeline, DB model diagram |
| Research Outcomes | ✅ Written — 6 subsections: DB resourcing, ORM/DAO, validation, ETL, backend design, testing, RBAC |
| Data Product Outcomes | ❌ Empty |
| Project Outcomes | ❌ Empty |
| Discussion of Findings | ❌ Empty |
| Recommendations & Conclusions | ❌ Empty |
| References | ⏳ Not yet written |
| Appendix / KSB Mapping | ⏳ Not yet written |

**Priority:** Complete the four empty sections. Each maps to specific ACs — see gaps below.

---

## SECTION 1 — KSB Evidence Map

### AC1 — K9, S1, S3 | User requirements → scalable, compliant data product

**Distinction:** Justify *why* the product met requirements and served multiple needs.

| Where | Detail |
| --- | --- |
| **Report (Scope)** | "serve multiple users through defined RBAC... scalable, secure solution" |
| **Report (Scope)** | "Early user requirements gathered from Assessment, Validation and Operations teams, translated to technical specs, refined via testing and research" |
| **Report (Research — RBAC)** | "RBAC designed to limit access to specific resources and actions — supporting principle of least privilege" |
| **Code** | `User` + `Role` models — three distinct roles map directly to real user groups |
| **Code** | `get_context` endpoint — frontend hydrated from token, not user-supplied form data |
| **Code** | `api_response()` decorator — consistent JSON envelope across all routes |
| ⚠️ **Gap** | Add in Discussion: *why* relational DB (referential integrity), *why* DAO (testability), GDPR compliance via audit trail |

---

### AC2 — K12, S2 | Business requirements + net-zero / sustainability

| Where | Detail |
| --- | --- |
| **Report (Scope)** | "aligns with organisational strategies for sustainable, maintainable systems... lowers unnecessary energy use" |
| **Report (Scope)** | Lean waste types named: Waiting, Transportation/Motion, Excess Processing |
| **Report (Scope)** | "prioritises reusable components (database schema and file ingestion scripts), minimises manual processing time" |
| ⚠️ **Gap** | Expand in Recommendations: Docker resource efficiency vs always-on infrastructure; net-zero policy alignment |

---

### AC3 — K7, S27 | Sustainable solutions, ESG, carbon reduction

| Where | Detail |
| --- | --- |
| **Report (Scope)** | "streamlined processes and reduced reliance upon on-premises, fragmented systems lowers unnecessary energy use" |
| **Code** | Normalised DB schema reduces redundant storage; Docker reduces environment overhead |
| ⚠️ **Gap** | Add in Discussion: containerisation reducing idle compute. Recommendations: managed cloud with renewable energy as future step |

---

### AC4 — K13, S4 | Security, scalability, governance in automated pipelines

**Strong evidence across report and code. Make prominent in presentation.**

| Where | Detail |
| --- | --- |
| **Report (Scope)** | FK constraints, transactional safety, rollbacks — "robust and auditable system" |
| **Report (Research — Validation)** | "differentiates between expected user errors and system errors... providing clear and actionable feedback" |
| **Report (Research — RBAC)** | "token-based link access... generated using secure hashes... encode permissions, data retrieval and expiry conditions" |
| **Code** | `submit()` — compensating transaction pattern: Files.com + PostgreSQL can't share a transaction boundary |
| **Code** | `handlers.py` — generic `HTTPException` handler with dynamic `e.status_code`; 401/403 without duplication |
| **Code** | `User` model — SHA-256 hash, `is_active` soft-disable, `centre_contact_id` scopes to specific person |
| **Code** | `Role` model — permissions as PostgreSQL ARRAY, `resource:action` convention |
| **Code** | `auth/dependencies.py` — `require_permission()` + `require_centre_permission()` as `Depends()` factories |
| **Code** | `config.py` — environment-driven config; pytest detection; secrets never hardcoded |
| **Design** | bcrypt vs SHA-256 — deliberate, documented rationale |
| **Design** | Dynamic URL permission derivation considered and rejected |

---

### AC5 — S5, B1 | Technical documentation + adapting to changing priorities

| Where | Detail |
| --- | --- |
| **Report (Research — DB resourcing)** | Supabase blocked → Docker; AWS SSH lacked tools — proactive adaptation documented |
| **Report (Research — Testing)** | BaseDAO refactor to fix hanging test runner |
| **Code** | Docstrings on every class and method; README full environment setup |
| **Code** | `.env.example` and `.env.name.example` — templated config files |
| ⚠️ **Gap** | Add in Discussion: mention README explicitly; note docs updated as design changed |

---

### AC6 — K6 | Debugging, version control, testing

| Where | Detail |
| --- | --- |
| **Report (Research — Testing)** | "TDD approach... Pytest with fixtures... unit tests... end-to-end tests simulate full API calls" |
| **Report (Research — Testing)** | Concrete example: SQLAlchemy sessions hanging → BaseDAO context manager refactor |
| **Report (Research — DB resourcing)** | "GitHub Actions to run automated tests on each push" |
| **Code** | 6 unit test files + endpoint tests; 13 test Excel registers; parametrized, async |
| **Code** | `conftest.py` — `reset_database`/`setup_database` for full test isolation |
| **Code** | `logger.py` — Rich handler, `--verbose` CLI flag for DEBUG/INFO switching |
| **Code** | `.github/workflows/docker-testing.yaml` — CI on every push; secrets-injected env |
| ⚠️ **Gap** | Add in Discussion: cause-and-effect — what testing *caught*, what CI *prevented*. Auth layer needs 401/403 tests |

---

### AC7 — K14 | On-demand cloud computing platforms

| Where | Detail |
| --- | --- |
| **Report (Research — DB resourcing)** | Supabase (blocked by Security), AWS SQL Server (lacked dev tools), Docker (chosen) |
| **Code** | Files.com as managed cloud PaaS file storage; PostgreSQL via Docker |
| ⚠️ **Gap** | Add in Discussion: Supabase (DBaaS) vs AWS RDS vs Docker — IaaS/PaaS/SaaS distinctions, trade-offs |

---

### AC8 — K8 | Deployment approaches for data pipelines

**Distinction (S16):** Evaluate algorithm success.

| Where | Detail |
| --- | --- |
| **Report (Research — DB resourcing)** | "containerising using Docker... GitHub Actions... more production-ready architecture, reproducible builds" |
| **Report (Scope)** | Docker + GitHub Actions enabling "consistent deployment across development, testing and production" |
| **Code** | `docker-compose.yml` — three services, environment-specific volumes, `profiles: ["testing"]` |
| **Code** | `submit()` — staged files → Files.com → compensating rollback → DB commit |
| **Code** | `.github/workflows/docker-testing.yaml` — full container build → test → teardown |
| ⚠️ **Distinction gap** | Evaluate `ingest_excel_file()` in Discussion: strengths (pipe chain, absent markers), weaknesses (`header=4` hardcoded, template-dependent, no OCR) |

---

### AC9 — K15 | Star schemas, data lakes, data marts, warehousing

| Where | Detail |
| --- | --- |
| **Scoping doc** | "Potential transformation of data into a star schema for reporting and analytics" |
| ⚠️ **Gap (not in report)** | Add to Discussion/Recommendations: current schema OLTP-optimised; star schema for Power BI analytics. Fact: candidate results. Dims: centre, version, window, examiner, language family |

---

### AC10 — K17, S6 | ETL — clean, validate, combine disparate sources

| Where | Detail |
| --- | --- |
| **Report (Research — ETL)** | "SQL queries and Python libraries (Pandas, Win32) to prepare CSV-formatted seed data... SQL Server, Excel workbooks, Word documents, text-based extracts" |
| **Report (Research — Validation)** | "Pandas for extraction and transformation — paired with Pydantic schemas to validate input" |
| **Code** | `ingest_excel_file()` pandas pipe chain: rename → drop → strip prefixes → strip strings → replace absents → construct IDs → replace NaNs |
| **Code** | `select_centre_contacts.sql` — CTE + `CROSS APPLY STRING_SPLIT` + `ROW_NUMBER()` normalising denormalised legacy data |
| **Code** | `setup_db.py` — walks multiple CSV directories |

---

### AC11 — K20 | Data engineering tools in own organisation

| Where | Detail |
| --- | --- |
| **Report (Research — Backend)** | "FastAPI... loosely structured MVC pattern... modular approach" |
| **Report (Research — ORM)** | "SQLalchemy as an ORM layer... DAO layer to keep logic modular and testable" |
| **Report (Research — Validation)** | "Pandas for extraction and transformation — paired with Pydantic schemas" |
| **Scoping doc** | Existing tools: PowerBI, SQL Server, Excel |
| **Code** | Full stack: FastAPI, SQLAlchemy, Pandas, Pydantic, Pytest, Docker, GitHub Actions, Files.com SDK, Rich, pyodbc |
| ⚠️ **Gap** | Add in Discussion: explicit contrast of existing vs new tools with justification; pyodbc as legacy bridge |

---

### AC12 — K24, K25, S24 | Evaluate prototypes; solution lifecycle

| Where | Detail |
| --- | --- |
| **Report (Research — DB resourcing)** | Supabase → Docker — infrastructure constraint identified, adapted |
| **Report (Research — ORM)** | "custom-generated UIDs... SQL Server vs PostgreSQL... differences in functions, data types and constraints" |
| **Report (Research — Testing)** | "I had not previously worked with Pytest for asynchronous and API testing — learning curve" |
| **Scoping doc** | Full lifecycle: Planning → Design → Development → Consultation → Training → Deployment → Maintenance |
| **Code** | Commented-out `@validates` approaches — shows iteration; `__init__`-based PK generation chosen deliberately |
| **Design** | Dynamic URL permission derivation evaluated and rejected |
| ⚠️ **Gap** | Make lifecycle explicit in Discussion. Name strengths AND weaknesses of current prototype state |

---

### AC13 — K26 | Approved organisational architectures and frameworks

| Where | Detail |
| --- | --- |
| **Scoping doc** | "Following the organisation's preference for relational databases" |
| **Code** | `pyodbc` — maintains compatibility with existing SQL Server infrastructure |
| ⚠️ **Gap** | Add in Discussion: alignment with org's SQL Server/PowerBI ecosystem; PEP 8; MVC architecture |

---

### AC14 — K4, S26 | Data quality metrics and frameworks

| Where | Detail |
| --- | --- |
| **Report (Scope)** | "ensuring Consistency, Accuracy, Completeness, Timeliness and Validity across all data sources" |
| **Report (Research — Validation)** | "flags specific errors for user correction before committing" — differentiates user vs system errors |
| **Code** | `validate_candidate()`, `check_for_duplicates()`, `validate_version()`, `check_lists()` |
| **Code** | `CandidateDAO.is_duplicate_candidate()` — three-case logic with `itertools.chain` |
| **Code** | DB-level constraints as last-line enforcement |
| ⚠️ **Gap** | Name DAMA framework explicitly in Discussion. Add tracking metrics to Project Outcomes |

---

### AC15 — K2, S9 | Query/manipulate data, automated validation, move between systems

| Where | Detail |
| --- | --- |
| **Report (Research — ETL)** | "SQL queries and Python libraries (Pandas, Win32) to prepare CSV-formatted seed data" |
| **Report (Research — ORM)** | "Wrote raw SQL queries, abstracted into ORM (SQLalchemy) for increased modularity" |
| **Code** | `base_dao.py` — dynamic ORM queries with AND conditions; reusable `select()` and `select_one()` |
| **Code** | `upload_dao.py` — nested object creation, version_id lookups, batch-candidate assignment |
| **Code** | `submit()` — temp filesystem → Files.com → PostgreSQL; `model_dump()` converts Pydantic → dict |
| **Code** | `select_centre_contacts.sql` — CTEs, `STRING_SPLIT`, `ROW_NUMBER()`, `UNION ALL` |

---

### AC16 — K19, S16 | Structured/semi-structured/unstructured data; extraction algorithms

**Distinction (S16):** Evaluate algorithm success.

| Where | Detail |
| --- | --- |
| **Report (Research — ETL)** | "SQL Server, Excel workbooks, Word documents, text-based extracts" — all three data types present |
| **Code** | `ingest_excel_file()` — semi-structured Excel: variable formatting, absent markers, prefix stripping |
| **Code** | PDF handling — unstructured binary staged for Files.com |
| **Code** | `select_centre_contacts.sql` — structured SQL + semi-structured input (semicolon-delimited emails) |
| ⚠️ **Gap** | Name all three data types explicitly in Discussion. Evaluate `ingest_excel_file()` for S16 distinction — `header=4` as weakness, OCR as future |

---

### AC17 — K30, S23 | Communicating about the data product to different audiences

**Distinction:** Evaluate the *impact* of communication.

| Where | Detail |
| --- | --- |
| **Report (Research — RBAC)** | References K30/S23 in brackets only — not developed |
| **Code** | `README.md` — step-by-step setup; `.env.example` for onboarding |
| **Code** | `api_response()` envelope — `{status, message, data}` for frontend consumption |
| ⚠️ **Gap (not in report)** | Write dedicated section. ER diagrams → technical; workflow diagrams → operational; work instructions → centres. Distinction: IT/Security conversation → Docker; Assessment → LanguageFamily in schema |

---

### AC18 — S22, B2 | Collaborative working with technical and non-technical stakeholders

| Where | Detail |
| --- | --- |
| **Scoping doc** | "Schedule meetings with Assessment, Validation, Operations and IT teams" |
| ⚠️ **Gap (not in report)** | Write dedicated section. Who you met, what was discussed, how feedback shaped decisions, communication style adaptation |

---

## SECTION 2 — Q&A Preparation

### "How did you ensure the data product met user requirements?" *(AC1)*

* Stakeholder interviews across Assessment, Validation, Operations → technical specs; refined via testing
* Three roles map to real user groups — scoped to only what they need; `get_context` locks context to token
* **Distinction:** *why* relational DB (referential integrity), *why* DAO (testability), *why* RBAC (least privilege)

---

### "How did you incorporate security and scalability?" *(AC4)*

* Magic-link tokens: `secrets.token_urlsafe(32)` → SHA-256 in DB — raw token never persists
* bcrypt for passwords vs SHA-256 for random tokens — deliberate rationale
* `resource:action` permissions via `Depends()` per route; 401 vs 403 distinction
* Dynamic URL permission derivation considered and rejected
* Compensating transaction in `submit()` — `successful_uploads` rollback on failure

---

### "How have testing, debugging and version control impacted your development?" *(AC6)*

* TDD — 6 unit test files + endpoint tests, 13 test registers, parametrized, async
* `conftest.py` — `reset_database`/`setup_database` for full test isolation
* GitHub Actions CI — full container build + test + teardown on every push
* BaseDAO session hang → `__enter__`/`__exit__` refactor — concrete debugging example
* Commented-out model iterations show deliberate design decisions in version history

---

### "What deployment approaches did you use?" *(AC8)*

* Docker Compose — dev/test/prod, `profiles: ["testing"]` isolates runner; GitHub Actions CI
* `submit()`: staged files → Files.com → compensating rollback → DB commit
* **S16 distinction:** `ingest_excel_file()` — strengths: pipe chain, absent markers; weakness: `header=4` hardcoded, template-dependent

---

### "Describe your ETL method" *(AC10)*

* Pandas pipe chain: rename → drop → strip prefixes → strip strings → replace absents → construct IDs → replace NaNs
* `check_lists()` — version, duplicate, date validation; field-level errors returned to user
* `select_centre_contacts.sql` — CTE, `STRING_SPLIT`, `ROW_NUMBER()` normalising denormalised legacy data

---

### "Which tools have you found most valuable?" *(AC11)*

* Pandas (pipe chain), SQLAlchemy (testable ORM), Pydantic (validation + model_dump()), Docker (reproducibility), pyodbc (legacy bridge)
* Contrast with org existing stack: SQL Server → PostgreSQL, Excel → structured API

---

### "What data quality metrics do you track?" *(AC14)*

* DAMA — Accuracy, Completeness, Consistency, Timeliness, Validity
* `is_duplicate_candidate()` — three-case logic including auto-renumbering
* Layered enforcement: Pandas → Pydantic → business rules → DB constraints

---

### "How do you tailor communication to different audiences?" *(AC17)*

* ER diagrams → technical; workflow diagrams → operational; work instructions → centres; README → developers
* **Distinction:** IT/Security conversation → Docker; Assessment input → LanguageFamily in schema

---

### "Describe a collaborative project with different stakeholders" *(AC18)*

* Assessment → Version/LanguageFamily tables; Operations → Upload/Batch/Candidate structure
* IT/Security constraint → Docker architecture; Manager → ongoing sign-off
* Adapted communication style per audience; actively sought constructive criticism

---

## SECTION 3 — Presentation Talking Points

| Slide | Key points | KSBs |
| --- | --- | --- |
| **Problem & Business Case** | Manual spreadsheets → integrity risks, no audit trail. KPIs quantify business case | S1, S2, K9 |
| **Solution Architecture** | Three-tier system. ER diagram. Normalised schema, RBAC, multi-user | S3, K13, K9 |
| **ETL Pipeline** | Excel → Pandas pipe chain → Pydantic → DAO → DB. Legacy SQL ETL (CTE/STRING_SPLIT) | K17, S6, K2, S9 |
| **Security & Governance** | RBAC + magic-link tokens. SHA-256 rationale. 401/403. Compensating transaction | K13, S4 |
| **Deployment & Testing** | Docker Compose (dev/test/prod). GitHub Actions CI. TDD Pytest. Rich logging | K6, K8, B1 |
| **Sustainability & Alignment** | Lean waste reduction. Reusable components. pyodbc legacy bridge | K7, K12, S27, K26 |
| **Evaluation & Future** | Prototype decisions. Design alternatives considered. Star schema, OCR roadmap | K24, K25, K15, S24 |

---

## GAPS SUMMARY — Prioritised Report Actions

| Priority | AC | KSB | Action |
| --- | --- | --- | --- |
| 🔴 High | — | — | Write Data Product Outcomes, Project Outcomes, Discussion, Recommendations sections |
| 🔴 High | AC18 | S22, B2 | Write Collaborative Working section |
| 🔴 High | AC17 | K30, S23 | Write Communication section + distinction impact |
| 🔴 High | AC9 | K15 | Add star schema paragraph in Discussion/Recommendations |
| 🟡 Medium | AC7 | K14 | Cloud platform comparison in Discussion: IaaS/PaaS/SaaS |
| 🟡 Medium | AC11 | K20 | Contrast existing vs new tools; pyodbc legacy bridge |
| 🟡 Medium | AC13 | K26 | Org SQL Server/PowerBI alignment; PEP 8 |
| 🟡 Medium | AC12 | K25 | Make lifecycle explicit; name prototype weaknesses |
| 🟢 Low | AC1 | K9 | Add *why* justifications in Discussion |
| 🟢 Low | AC16 | S16 | Evaluate `ingest_excel_file()` for distinction; `header=4` as weakness |
| 🟢 Low | AC14 | K4 | Name DAMA framework explicitly |
| 🟢 Low | AC6 | K6 | Cause-and-effect: what testing caught, what CI prevented |

---

## STILL TO BUILD — Auth Implementation Tracker

| Item | Status |
| --- | --- |
| `User` + `Role` models | ✅ Done |
| `User.@validates('token_hash')` | ⚠️ Bug — needs `@validates('token_hash')` field name |
| Seed CSV files (roles + users) | ✅ Done |
| `get_db()` generator, auth dependencies, upload routes | ✅ Done |
| `get_context` endpoint | ✅ Done |
| `UploadPayload` + `UploadFileData` cleaned up | ✅ Done |
| `parse_pg_array()` in seeder | ⏳ To do |
| Token hashing in seeder | ⏳ To do |
| 401/403 tests | ⏳ To do |
| `joinedload(CentreContact.centre)` — fix syntax | ⚠️ Minor bug |

---

*Last updated: essay content reviewed and folded into evidence map. Report status overview added. Four empty report sections flagged as highest priority.*
