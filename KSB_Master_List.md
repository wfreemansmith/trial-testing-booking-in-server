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
|-------|--------|
| **Report** | Scope: "serve multiple users through defined RBAC... scalable, secure solution" |
| **Report** | "Early user requirements gathered from Assessment, Validation and Operations teams, translated to technical specs, refined via testing and research" |
| **Code** | `models/__init__.py` — schema serves multiple user types (centres, examiners, IELTS staff, managers) |
| **Code** | Pydantic schemas enforce consistent data contracts across all user-facing API boundaries |
| **Code** | `get_context` endpoint derives `centre_id` and `marking_window_id` from the token, not form data — prevents a centre user from submitting on behalf of another centre |
| ⚠️ **Gap** | Add explicit justification: *why* relational DB over alternatives, *why* DAO pattern over raw SQL. Link each to a specific requirement. Mention GDPR compliance via access controls + audit trail |

---

### AC2 — K12, S2 | Business requirements + net-zero / sustainability
| Where | Detail |
|-------|--------|
| **Report** | Scope: "aligns with organisational strategies for sustainable, maintainable systems... contributes to cost efficiency... lowers unnecessary energy use" |
| **Report** | KPIs include time saved, waste reduction (Lean waste types: Waiting, Transportation/Motion, Excess Processing) |
| ⚠️ **Gap** | Mention assessing existing solution's inefficiencies. Reference Docker's resource efficiency vs always-on infrastructure |

---

### AC3 — K7, S27 | Sustainable solutions, ESG, carbon reduction
| Where | Detail |
|-------|--------|
| **Report** | Scope: reusable components, reduced reliance on fragmented on-premises systems |
| **Code** | Normalised DB schema reduces redundant storage; Docker reduces environment overhead |
| ⚠️ **Gap** | Add a sentence on containerisation reducing idle compute. Mention managed cloud with renewable energy as a future step |

---

### AC4 — K13, S4 | Security, scalability, governance in automated pipelines
**Strong evidence — make prominent in report and presentation.**

| Where | Detail |
|-------|--------|
| **Report** | "Role Based and Tokenised Access" — RBAC + token security, least privilege, data protection |
| **Report** | "Validation, error handling" — differentiates user vs system errors |
| **Code** | `submit()` — **compensating transaction pattern**: Files.com + PostgreSQL can't share a transaction boundary; `successful_uploads` tracks partial state, rolled back on failure |
| **Code** | `handlers.py` — structured HTTP error responses (400/415/422/500) |
| **Code** | `models/__init__.py` — FK constraints, `CheckConstraint` on `centre_id`, `nullable=False` |
| **Code** | `auth/dependencies.py` — `require_permission()` and `require_centre_permission()`: FastAPI dependency factories. `require_centre_permission` additionally asserts the user has a linked centre contact before proceeding |
| **Code** | `Role` model — permissions stored as PostgreSQL `ARRAY(String)` using `resource:action` convention (e.g. `upload:write`) |
| **Code** | `User.token_hash` — SHA-256 hashed on write; `@validates` guard prevents double-hashing on DB load |
| **Design decision** | Dynamic URL-based permission derivation was explicitly considered and rejected in favour of `resource:action` strings — more maintainable, auditable, independently testable |
| **Conversation** | K13 + K8 explicitly flagged for compensating transaction / distributed system pattern in `submit()` |

---

### AC5 — S5, B1 | Technical documentation + adapting to changing priorities
| Where | Detail |
|-------|--------|
| **Report** | "Database resourcing" — proactively adapted when Supabase blocked, when AWS SSH lacked tools |
| **Report** | "Testing Approach" — refactored BaseDAO to fix hanging test runner |
| **Code** | Docstrings on every class and method; README covers environment setup, Docker, env vars |
| **Code** | `.env.example` and `_env_name.example` document all required configuration variables |
| **Code** | `KSB_Master_List.md` and `EPA_Interview_Prep.md` version-controlled in the repo as living assessment documents |
| ⚠️ **Gap** | Explicitly mention README in report. Note documentation updated as design changed (schema changes, DAO refactor, RBAC addition) |

---

### AC6 — K6 | Debugging, version control, testing impact on software development
| Where | Detail |
|-------|--------|
| **Report** | "Testing Approach & Version Control" — TDD, Pytest, fixtures, Git, GitHub Actions CI |
| **Report** | Concrete debugging example: BaseDAO `__enter__`/`__exit__` refactor to fix hanging test runner |
| **Code** | `testing/endpoint_tests/test_upload.py` — parametrized tests, async client, 200/400/401/415/422 coverage |
| **Code** | `conftest.py` — fixtures reset and reseed DB per test for full isolation |
| **CI** | GitHub Actions `docker-testing.yaml` — full suite runs on every push. An `os.walk` file-ordering bug caused FK violations in CI (languages seeded before language_families) but was invisible locally; fixed with `sorted()`. CI is now passing. This is a concrete example of CI catching an environment-specific bug |
| ⚠️ **Gap** | Add cause-and-effect in report: what did testing *catch*? What did version control *enable*? The CI bug story is a strong concrete example |

---

### AC7 — K14 | On-demand cloud computing platforms
| Where | Detail |
|-------|--------|
| **Report** | "Database resourcing" — evaluated Supabase (blocked by Security), AWS SQL Server (lacked dev tools) |
| **Code** | Files.com as managed cloud file storage (PaaS); PostgreSQL via Docker |
| ⚠️ **Gap (weak KSB)** | Add explicit comparison: Supabase (DBaaS/PaaS) vs AWS RDS (PaaS) vs Docker PostgreSQL (IaaS) — trade-offs of cost, control, security, compliance. Mention IaaS/PaaS/SaaS distinctions. Files.com as PaaS file storage |

---

### AC8 — K8 | Deployment approaches for data pipelines
**Distinction (S16):** Evaluate the success of the algorithm — metrics, accuracy, improvement areas.

| Where | Detail |
|-------|--------|
| **Report** | "Database resourcing" — Docker Compose with dev/test/prod; GitHub Actions CI |
| **Code** | `docker-compose.yml` — three services (db, server, tests), environment-specific volumes, test runner in separate profile |
| **Code** | `submit()` — full automated pipeline: retrieve staged files → upload to Files.com → rollback on failure → DB commit |
| **CI** | GitHub Actions passing — `sorted()` fix resolved non-deterministic seed order across environments |
| **Conversation** | K8 explicitly noted for `submit()` pipeline orchestration |
| ⚠️ **Distinction gap** | Evaluate `ingest_excel_file()` algorithm: strengths (handles absent markers, prefix stripping, semi-structured input), weaknesses (template-dependent, `header=4` hardcoded). What metrics could you track (processing time, error rate before/after)? |

---

### AC9 — K15 | Star schemas, data lakes, data marts, warehousing
| Where | Detail |
|-------|--------|
| **Scoping doc** | "Potential transformation of data into a star schema for reporting and analytics" |
| ⚠️ **Gap** | Not in report yet. Add to Discussion or Recommendations: current normalised schema is OLTP-optimised; for analytics/Power BI a star schema would be appropriate. Fact table: candidate results. Dims: centre, version, window, examiner, language family |

---

### AC10 — K17, S6 | ETL — clean, validate, combine disparate sources
| Where | Detail |
|-------|--------|
| **Report** | "Extracting and Preparing Seed Data" — integrated SQL Server, Excel, Word docs, text extracts → CSV seed format |
| **Code** | `excel_register_processing.py` — `rename_columns` → `drop_empty_rows` → `strip_prefixes` → `strip_strings` → `replace_absent_candidates` → `construct_version_ids` → `replace_nans` |
| **Code** | `setup_db.py` — walks multiple CSV directories to seed from combined sources; `sorted()` ensures deterministic FK-safe insertion order |

---

### AC11 — K20 | Data engineering tools in own organisation
| Where | Detail |
|-------|--------|
| **Scoping doc** | Existing tools: PowerBI, SQL Server, Excel |
| **Code** | New stack: FastAPI, SQLAlchemy, Pandas, Pydantic, Pytest, Docker, GitHub Actions, Files.com SDK |
| ⚠️ **Gap** | Add to report — contrast existing vs new tools with justification. E.g. Pandas over raw SQL for Excel ingestion; SQLAlchemy ORM for modularity and testability |

---

### AC12 — K24, K25, S24 | Evaluate prototypes; solution lifecycle
| Where | Detail |
|-------|--------|
| **Report** | "Database resourcing" — Supabase → Docker lifecycle journey |
| **Report** | "ORM and DAO" — SQL Server vs PostgreSQL; custom UIDs vs integer PKs |
| **Scoping doc** | Full lifecycle: Planning → Design → Development → Consultation → Training → Deployment → Maintenance |
| **Design decision** | RBAC permission model: dynamic URL-based derivation evaluated and explicitly rejected in favour of `resource:action` strings. Documented as a deliberate design decision for the report |
| **Retrospective** | RBAC was retrofitted rather than designed in from the start — required costly changes to models, seed infrastructure, route signatures, test suite, and conftest. Lesson: access control requirements should be elicited in stakeholder analysis and built into the initial design |
| **Retrospective** | Building from scratch with FastAPI/SQLAlchemy was ambitious and evidences breadth of technical skill, but in a different context a low-code orchestration tool (n8n, Apache Airflow, Azure Data Factory, Prefect) could deliver equivalent pipeline outcomes faster, allowing focus on business logic rather than infrastructure. ADF is particularly relevant given CUP's Microsoft ecosystem |
| ⚠️ **Gap** | Make lifecycle explicit in Discussion of Findings. Name strengths AND weaknesses of current prototype state. Include both retrospective reflections — they demonstrate honest self-evaluation (S24, K25) |

---

### AC13 — K26 | Approved organisational architectures and frameworks
| Where | Detail |
|-------|--------|
| **Scoping doc** | "Following the organisation's preference for relational databases" |
| ⚠️ **Gap** | Add a sentence on aligning with org's SQL Server/PowerBI ecosystem. Mention Agile/sprint delivery if applicable at CUP |

---

### AC14 — K4, S26 | Data quality metrics and frameworks
| Where | Detail |
|-------|--------|
| **Report** | Scope: "ensuring Consistency, Accuracy, Completeness, Timeliness and Validity" |
| **Code** | `validate_candidate()` — checks `candidate_name` not blank (Completeness); correct format (Accuracy) |
| **Code** | `check_for_duplicates()` — boolean mask across incoming candidates; three-case logic: full duplicate / number-only conflict / new candidate (Uniqueness) |
| **Code** | `validate_version()` — validates version IDs against database (Validity) |
| **Code** | `check_lists()` — `test_date` not in future check; marking window expiry via auth dependency (Timeliness) |
| **Code** | `construct_upload_filename()` / `construct_upload_path()` in `helpful_funcs.py` — agreed naming convention enforced cross-system (Consistency) |
| **Code** | Compensating transaction in `submit()` — Files.com + PostgreSQL cannot share a transaction boundary; `successful_uploads` rolled back on failure (Consistency) |
| **Code** | `models/__init__.py` — FK constraints, `CheckConstraint` on `centre_id`, `nullable=False` — DB-level last-line enforcement |
| **README** | ✅ Data quality section added — all six DAMA dimensions mapped to specific code mechanisms |
| ~~⚠️ **Gap**~~ | ~~Name the DAMA framework explicitly~~ — **Done** |

---

### AC15 — K2, S9 | Query/manipulate data, automated validation, move between systems
| Where | Detail |
|-------|--------|
| **Report** | "Extracting and Preparing Seed Data" — SQL + Pandas + Win32 for legacy extraction |
| **Code** | `base_dao.py` — dynamic SQLAlchemy ORM queries with AND conditions |
| **Code** | `upload_dao.py` — complex nested object creation; version_id lookups; batch-candidate assignment |
| **Code** | `submit()` — moves data: temp filesystem → Files.com → PostgreSQL |

---

### AC16 — K19, S16 | Structured/semi-structured/unstructured data; extraction algorithms
**Distinction (S16):** Evaluate algorithm success — metrics, strengths, weaknesses, improvements.

| Where | Detail |
|-------|--------|
| **Code** | `excel_register_processing.py` — `ingest_excel_file()` handles semi-structured Excel |
| **Code** | `upload_routes.py` — PDF handling (unstructured binary) staged for Files.com |
| **Report** | "Extracting and Preparing Seed Data" — Word docs, text extracts as unstructured sources |
| ⚠️ **Gap** | Explicitly name the three data types in report. For S16 distinction: evaluate `ingest_excel_file()` — strengths (absent markers, prefix stripping), weaknesses (template-dependent, `header=4` hardcoded). Reference scoping doc's OCR/CV future suggestion |

---

### AC17 — K30, S23 | Communicating about the data product to different audiences
**Distinction:** Evaluate the *impact* of communication — did it lead to understanding, action, decisions?

| Where | Detail |
|-------|--------|
| **Report** | "Role Based and Tokenised Access" — references K30/S23 |
| ⚠️ **Gap** | Needs a dedicated section. Describe: ER diagrams for technical stakeholders, workflow diagrams for operational staff, non-technical instructions for centres. For distinction: what *changed* as a result of communication? |

---

### AC18 — S22, B2 | Collaborative working with technical and non-technical stakeholders
| Where | Detail |
|-------|--------|
| **Scoping doc** | "Schedule meetings with Assessment, Validation, Operations and IT teams" |
| ⚠️ **Gap** | Not in report yet — needs a dedicated section. Include: who you met, what was discussed, how feedback shaped decisions (e.g. IT Security blocking Supabase → Docker; Assessment team input → LanguageFamily in schema), how you adapted communication style |

---

## SECTION 2 — Q&A Preparation

### "How did you ensure the data product met user requirements and regulatory compliance?" *(AC1 — K9, S1, S3)*
- Stakeholder interviews → technical specs; requirements refined via testing
- RBAC + tokenised access for GDPR and data protection
- `get_context` endpoint — `centre_id` and `marking_window_id` derived from token, not form data; prevents cross-centre data tampering
- Pydantic validation at API boundary; FK constraints + rollbacks for integrity
- **Distinction:** justify *why* — relational DB for referential integrity, DAO for testability

---

### "Describe how sustainable, net-zero technologies were considered" *(AC2/3 — K12, K7, S2, S27)*
- Replacing manual processes reduces Lean waste (Waiting, Motion, Excess Processing)
- Normalised schema reduces storage vs duplicated spreadsheets
- Docker avoids always-on infrastructure; reproducible builds reduce wasted compute
- Future: managed cloud with renewable energy commitments as next step

---

### "How did you incorporate security and scalability into your data pipelines?" *(AC4 — K13, S4)*
- RBAC + tokenised links — least privilege, time-limited access, marking window expiry check
- `resource:action` permission convention — explicit, auditable, independently testable; dynamic URL-based derivation explicitly rejected
- Pydantic validation at every API boundary
- FK constraints and transactional rollbacks at DB level
- **Compensating transaction pattern in `submit()`** — distributed system integrity; `successful_uploads` rollback on failure
- Docker for scalable, consistent deployment

---

### "How have debugging, version control and testing impacted your development?" *(AC6 — K6)*
- TDD from the start — Pytest unit + endpoint tests, parametrized, async
- Git for version control; GitHub Actions CI — caught an `os.walk` file-ordering bug causing FK violations in CI (invisible locally); fixed with `sorted()`; suite now fully passing
- Concrete debugging: SQLAlchemy sessions hanging → refactored BaseDAO context manager
- Structured Python `logging` for runtime debugging

---

### "What deployment approaches did you use and why?" *(AC8 — K8)*
- Docker Compose — dev/test/prod, solved infrastructure blocker
- GitHub Actions CI/CD — automated testing on every push, now passing
- `submit()` orchestrates runtime pipeline: staged files → Files.com → compensating rollback → DB commit
- **Distinction (S16):** `ingest_excel_file()` — handles variable formatting; weakness is `header=4` hardcoded template dependency

---

### "Describe your ETL method for cleaning and validating data" *(AC10 — K17, S6)*
- `ingest_excel_file()` pipeline: rename → drop empties → strip prefixes → strip strings → replace absents → construct IDs → replace NaNs
- Pydantic as validation layer after Pandas transformation
- `check_lists()` — version validation, duplicate checking, error flagging before DB commit
- Legacy ETL: SQL + Pandas + Win32 → CSV seed data from SQL Server, Excel, Word

---

### "Which data engineering tools have you found most valuable?" *(AC11 — K20)*
- **Pandas** — flexible semi-structured Excel ingestion
- **SQLAlchemy ORM** — type-safe, modular, cross-engine compatible
- **Pydantic** — validation + clean user-facing error messages
- **Docker** — solved infrastructure constraint, reproducible environments
- Compared to org's existing tools: SQL Server → PostgreSQL, Excel → structured API

---

### "How do you evaluate prototype strengths and weaknesses?" *(AC12 — K24, K25, S24)*
- Supabase → Docker: identified infrastructure constraint early, adapted
- RBAC permission model: dynamic URL-based derivation evaluated and rejected — explicit `resource:action` strings are more maintainable and auditable. A documented deliberate design decision
- SQL Server vs PostgreSQL: evaluated Docker compatibility, constraint differences
- Custom UIDs vs integer PKs: deliberate trade-off — human-readable for non-technical staff
- Test suite as formal evaluation mechanism
- Weakness: proof-of-concept, not production-hardened; training and front-end still needed
- **Retrospective — RBAC timing:** Retrofitting RBAC required changes across models, seed data, route signatures, test suite, and conftest. Had access control requirements been elicited earlier in stakeholder analysis, this rework could have been avoided. Lesson: security design belongs in the initial architecture phase
- **Retrospective — build vs configure:** Building from scratch evidences depth of technical skill, but in a different organisational context, a low-code orchestration tool (n8n, Apache Airflow, Azure Data Factory, Prefect) could deliver equivalent pipeline outcomes with less infrastructure overhead. Azure Data Factory is particularly relevant given CUP's Microsoft ecosystem. The choice to build from scratch was appropriate for demonstrating breadth of data engineering skills and for the sensitivity/control requirements of candidate data

---

### "What data quality metrics do you track?" *(AC14 — K4, S26)*
- Five dimensions: Consistency, Accuracy, Completeness, Timeliness, Validity (DAMA framework)
- KPIs: time per batch, turnaround, error rate, data accessibility
- Validation flags in API response — user-correctable before commit
- DB constraints as last-line enforcement

---

### "How do you tailor communication to different audiences?" *(AC17 — K30, S23)*
- ER diagrams → technical stakeholders; workflow diagrams → operational staff
- README + docs → developers; non-technical work instructions → centre users
- **Distinction:** reflect on impact — did communication lead to a decision or requirement change?

---

### "Describe a collaborative project with different stakeholders" *(AC18 — S22, B2)*
- Requirements gathering: Assessment, Validation, Operations, IT/Security
- IT/Security constraint directly shaped Docker architecture decision
- Schema design informed by operational team workflows; LanguageFamily added from Assessment team input
- Adapted communication style: technical detail for IT, process-level for operational teams

---

## SECTION 3 — Presentation Talking Points

| Slide | Key points | KSBs |
|-------|-----------|------|
| **Problem & Business Case** | Manual spreadsheets → integrity risks, no audit trail. KPIs quantify business case | S1, S2, K9 |
| **Solution Architecture** | Three-tier system. ER diagram. Normalised schema, RBAC, multi-user | S3, K13, K9 |
| **ETL Pipeline** | Excel → Pandas → Pydantic → DAO → DB. Legacy ETL. Error handling flow | K17, S6, K2, S9 |
| **Security & Governance** | RBAC + tokens. `resource:action` convention. Compensating transaction in `submit()`. HTTP error hierarchy | K13, S4 |
| **Deployment & Testing** | Docker Compose. GitHub Actions CI (passing). TDD Pytest. Proactive infrastructure fix | K6, K8, B1 |
| **Sustainability & Alignment** | Lean waste reduction. Reusable components. Org ecosystem alignment | K7, K12, S27, K26 |
| **Evaluation & Future** | Prototype decisions. Path to production. Star schema, front-end, OCR roadmap | K24, K25, K15, S24 |

---

## GAPS SUMMARY — Prioritised Report Actions

| Priority | AC | KSB | Action |
|----------|----|-----|--------|
| 🔴 High | AC18 | S22, B2 | Add collaborative working section — who, discussions, how feedback shaped decisions |
| 🔴 High | AC17 | K30, S23 | Add communication section + distinction reflection on impact |
| 🔴 High | AC9 | K15 | Add star schema paragraph in Discussion/Recommendations |
| 🟡 Medium | AC7 | K14 | Cloud platform comparison — Supabase vs AWS vs Docker, IaaS/PaaS/SaaS |
| 🟡 Medium | AC11 | K20 | Contrast existing org tools vs new stack with justification |
| 🟡 Medium | AC13 | K26 | Add sentence on org architecture alignment |
| 🟡 Medium | AC12 | K25, S24 | Make lifecycle journey explicit in Discussion of Findings; include both retrospective reflections (RBAC timing; build vs configure) as honest prototype evaluation — maps directly to S24 |
| 🟢 Low | AC5 | S5 | Mention README and version-controlled docs explicitly |
| 🟢 Low | AC16 | K19 | Name structured/semi-structured/unstructured types in report |
| 🟢 Low | AC8/16 | S16 | Evaluate `ingest_excel_file()` algorithm for distinction |
| 🟢 Low | AC14 | K4 | Name DAMA framework for data quality dimensions |
| 🟢 Low | AC6 | K6 | Add CI bug (`sorted()`) as concrete cause-and-effect testing example |

---

## PRE-SUBMISSION CHECKLIST

Track outstanding work before report submission. Tick off each item as completed — update this doc and commit.

### Codebase tasks
| Done | Task | AC | KSB |
|------|------|----|-----|
| ✅ | README: Add data quality metrics section — DAMA framework (six dimensions), where each dimension is enforced in code | AC14 | K4 |
| ☐ | README: Add `Future: Analytical Layer` section sketching proposed star schema (fact/dim tables from existing model) | AC9 | K15 |
| ☐ | CHANGELOG or commit note documenting the RBAC retrofit — what changed and why *(optional but strengthens K6 story)* | AC6 | K6 |

### Evidence gathering (outside codebase)
| Done | Task | AC | KSB |
|------|------|----|-----|
| ☐ | Produce ER diagram for the schema (dbdiagram.io or draw.io) — communication artefact for stakeholder discussions | AC17 | K30, S23 |
| ☐ | Document rough time/effort estimate: current manual process vs new system per batch — quantifiable KPI evidence | AC14, AC2 | K4, K12 |
| ☐ | Identify and document real informal stakeholder interactions (Slack, email, Teams) as S22/B2 evidence — do not fabricate; draw on conversations that actually happened | AC18 | S22, B2 |

### Report sections to write
| Done | Task | AC | KSB |
|------|------|----|-----|
| ☐ | Collaborative working section — who, what was discussed, how feedback shaped decisions | AC18 | S22, B2 |
| ☐ | Communication section + distinction: what *changed* as a result of communication | AC17 | K30, S23 |
| ☐ | Cloud platform comparison paragraph — Supabase vs AWS vs Docker, IaaS/PaaS/SaaS | AC7 | K14 |
| ☐ | Tools contrast paragraph — existing org tools vs new stack with justification | AC11 | K20 |
| ☐ | Org architecture alignment sentence — SQL Server/Power BI ecosystem fit | AC13 | K26 |
| ☐ | Discussion of Findings: lifecycle section — prototype decisions, RBAC retrospective, build vs configure reflection | AC12 | K25, S24 |
| ☐ | Recommendations: star schema paragraph — current OLTP schema → future analytical layer | AC9 | K15 |
| ☐ | Name DAMA framework (six dimensions) explicitly in data quality section | AC14 | K4 |
| ☐ | Name structured/semi-structured/unstructured data types explicitly | AC16 | K19 |
| ☐ | Evaluate `ingest_excel_file()` algorithm — strengths, weaknesses, future (distinction) | AC8, AC16 | S16 |
| ☐ | CI bug story (`sorted()`) as cause-and-effect testing example | AC6 | K6 |

---

*Last updated: RBAC auth system completed — `User`/`Role` models, magic-link `?q=` token pattern, SHA-256 hashing, `require_permission`/`require_centre_permission` dependency factories, `resource:action` convention, `get_context` endpoint, seed CSVs. GitHub Actions CI now passing (after `sorted()` fix for `os.walk` non-determinism). Test suite fully passing — 57 tests including mocked Files.com submit tests. Retrospective reflections added: (1) RBAC should be designed in from the start; (2) in a different context, low-code orchestration tools (n8n, Airflow, Azure Data Factory, Prefect) could deliver equivalent outcomes faster — both map to AC12 (K24, K25, S24).*
