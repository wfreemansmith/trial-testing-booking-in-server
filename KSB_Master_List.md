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
| **Code** | `User` + `Role` models — RBAC design directly maps to multi-user requirement; each user type (centre_admin, staff, master) has scoped access reflecting their operational role |
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
| **Report** | "Validation, error handling" — differentiates user vs system errors |
| **Code** | `submit()` — **compensating transaction pattern**: Files.com + PostgreSQL can't share a transaction boundary; `successful_uploads` tracks partial state, rolled back on failure |
| **Code** | `handlers.py` — structured HTTP error responses (400/415/422/500) |
| **Code** | `models/__init__.py` — FK constraints, `CheckConstraint` on `centre_id`, `nullable=False` |
| **Code** | `User` model — `token_hash` (SHA-256, never raw token stored), `is_active` for soft-disable, `centre_contact_id` scoping access to a specific person not just a centre |
| **Code** | `Role` model — `permissions` as PostgreSQL `ARRAY(String)`, `resource:action` convention (e.g. `upload:write`) enables fine-grained per-route checks |
| **Code** | `auth/dependencies.py` (planned) — FastAPI `Depends()` injects permission check per route; 403 raised before handler runs if permission absent |
| **Design** | Magic-link / query-token pattern: token generated with `secrets.token_urlsafe(32)`, SHA-256 hashed before DB storage; raw token never persists anywhere |
| **Design** | Distinction between hashing strategies: bcrypt (slow, salted) for passwords vs SHA-256 (fast) for random tokens — documented rationale for your report |
| **Conversation** | K13 + K8 explicitly flagged for compensating transaction / distributed system pattern in `submit()` |

---

### AC5 — S5, B1 | Technical documentation + adapting to changing priorities

| Where | Detail |
| --- | --- |
| **Report** | "Database resourcing" — proactively adapted when Supabase blocked, when AWS SSH lacked tools |
| **Report** | "Testing Approach" — refactored BaseDAO to fix hanging test runner |
| **Code** | Docstrings on every class and method; README covers environment setup, Docker, env vars |
| **Code** | `User` and `Role` models include class-level docstrings consistent with existing model documentation pattern |
| ⚠️ **Gap** | Explicitly mention README in report. Note documentation updated as design changed (schema changes, DAO refactor) |

---

### AC6 — K6 | Debugging, version control, testing impact on software development

| Where | Detail |
| --- | --- |
| **Report** | "Testing Approach & Version Control" — TDD, Pytest, fixtures, Git, GitHub Actions CI |
| **Report** | Concrete debugging example: BaseDAO `__enter__`/`__exit__` refactor to fix hanging test runner |
| **Code** | `testing/endpoint_tests/test_upload.py` — parametrized tests, async client, 200/400/415/422 coverage |
| ⚠️ **Gap** | Add cause-and-effect: what did testing *catch*? What did version control *enable*? Don't just describe — show impact |

---

### AC7 — K14 | On-demand cloud computing platforms

| Where | Detail |
| --- | --- |
| **Report** | "Database resourcing" — evaluated Supabase (blocked by Security), AWS SQL Server (lacked dev tools) |
| **Code** | Files.com as managed cloud file storage; PostgreSQL via Docker |
| ⚠️ **Gap (weak KSB)** | Add explicit comparison: Supabase (DBaaS) vs AWS RDS vs Docker PostgreSQL — trade-offs of cost, control, security. Mention IaaS/PaaS/SaaS distinctions. Files.com as PaaS file storage |

---

### AC8 — K8 | Deployment approaches for data pipelines

**Distinction (S16):** Evaluate the success of the algorithm — metrics, accuracy, improvement areas.

| Where | Detail |
| --- | --- |
| **Report** | "Database resourcing" — Docker Compose with dev/test/prod; GitHub Actions CI |
| **Code** | `docker-compose.yml` — three services, environment-specific volumes |
| **Code** | `submit()` — full automated pipeline: retrieve staged files → upload to Files.com → rollback on failure → DB commit |
| **Conversation** | K8 explicitly noted for `submit()` pipeline orchestration |
| ⚠️ **Distinction gap** | Evaluate `ingest_excel_file()` algorithm: strengths (handles absent markers, prefix stripping, semi-structured input), weaknesses (template-dependent, no OCR). What metrics could you track (processing time, error rate before/after)? |

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
| **Code** | `excel_register_processing.py` — `rename_columns` → `drop_empty_rows` → `strip_prefixes` → `strip_strings` → `replace_absent_candidates` → `construct_version_ids` → `replace_nans` |
| **Code** | `setup_db.py` — walks multiple CSV directories to seed from combined sources |

---

### AC11 — K20 | Data engineering tools in own organisation

| Where | Detail |
| --- | --- |
| **Scoping doc** | Existing tools: PowerBI, SQL Server, Excel |
| **Code** | New stack: FastAPI, SQLAlchemy, Pandas, Pydantic, Pytest, Docker, GitHub Actions, Files.com SDK |
| ⚠️ **Gap** | Add to report — contrast existing vs new tools with justification. E.g. Pandas over raw SQL for Excel ingestion; SQLAlchemy ORM for modularity and testability |

---

### AC12 — K24, K25, S24 | Evaluate prototypes; solution lifecycle

| Where | Detail |
| --- | --- |
| **Report** | "Database resourcing" — Supabase → Docker lifecycle journey |
| **Report** | "ORM and DAO" — SQL Server vs PostgreSQL; custom UIDs vs integer PKs |
| **Scoping doc** | Full lifecycle: Planning → Design → Development → Consultation → Training → Deployment → Maintenance |
| ⚠️ **Gap** | Make lifecycle explicit in Discussion of Findings. Name strengths AND weaknesses of current prototype state |

---

### AC13 — K26 | Approved organisational architectures and frameworks

| Where | Detail |
| --- | --- |
| **Scoping doc** | "Following the organisation's preference for relational databases" |
| ⚠️ **Gap** | Add a sentence on aligning with org's SQL Server/PowerBI ecosystem. Mention Agile/sprint delivery if applicable at CUP |

---

### AC14 — K4, S26 | Data quality metrics and frameworks

| Where | Detail |
| --- | --- |
| **Report** | Scope: "ensuring Consistency, Accuracy, Completeness, Timeliness and Validity" |
| **Code** | `excel_register_processing.py` — `validate_candidate()`, `check_for_duplicates()`, `validate_version()`, `check_lists()` |
| **Code** | `models/__init__.py` — DB-level constraints as last-line quality enforcement |
| ⚠️ **Gap** | Name the DAMA framework explicitly — your five dimensions match it. Shows theoretical grounding |

---

### AC15 — K2, S9 | Query/manipulate data, automated validation, move between systems

| Where | Detail |
| --- | --- |
| **Report** | "Extracting and Preparing Seed Data" — SQL + Pandas + Win32 for legacy extraction |
| **Code** | `base_dao.py` — dynamic SQLAlchemy ORM queries with AND conditions |
| **Code** | `upload_dao.py` — complex nested object creation; version_id lookups; batch-candidate assignment |
| **Code** | `submit()` — moves data: temp filesystem → Files.com → PostgreSQL |

---

### AC16 — K19, S16 | Structured/semi-structured/unstructured data; extraction algorithms

**Distinction (S16):** Evaluate algorithm success — metrics, strengths, weaknesses, improvements.

| Where | Detail |
| --- | --- |
| **Code** | `excel_register_processing.py` — `ingest_excel_file()` handles semi-structured Excel |
| **Code** | `upload_routes.py` — PDF handling (unstructured binary) staged for Files.com |
| **Report** | "Extracting and Preparing Seed Data" — Word docs, text extracts as unstructured sources |
| ⚠️ **Gap** | Explicitly name the three data types in report. For S16 distinction: evaluate `ingest_excel_file()` — strengths (absent markers, prefix stripping), weaknesses (template-dependent, no OCR). Reference scoping doc's OCR/CV future suggestion |

---

### AC17 — K30, S23 | Communicating about the data product to different audiences

**Distinction:** Evaluate the *impact* of communication — did it lead to understanding, action, decisions?

| Where | Detail |
| --- | --- |
| **Report** | "Role Based and Tokenised Access" — references K30/S23 |
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
* RBAC + tokenised access for GDPR and data protection
* Three distinct roles (centre_admin, staff, master) map directly to real user groups — each scoped to only what they need
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
* Distinction between bcrypt (passwords — slow, salted, brute-force resistant) and SHA-256 (random tokens — fast, sufficient because token entropy is already high)
* Permissions stored as PostgreSQL ARRAY on Role model — `resource:action` convention, checked via FastAPI `Depends()` per route
* `is_active` flag allows soft-disabling users without breaking audit trail — GDPR-aligned
* `centre_contact_id` FK scopes a centre user to a specific person, not just a centre — tighter access control
* FK constraints and transactional rollbacks at DB level
* **Compensating transaction pattern in `submit()`** — distributed system integrity; `successful_uploads` rollback on failure
* Docker for scalable, consistent deployment

---

### "How have debugging, version control and testing impacted your development?" *(AC6 — K6)*

* TDD from the start — Pytest unit + endpoint tests, parametrized, async
* Git for version control; GitHub Actions CI — caught environment issues early
* Concrete debugging: SQLAlchemy sessions hanging → refactored BaseDAO context manager
* Structured Python `logging` for runtime debugging

---

### "What deployment approaches did you use and why?" *(AC8 — K8)*

* Docker Compose — dev/test/prod, solved infrastructure blocker
* GitHub Actions CI/CD — automated testing on push
* `submit()` orchestrates runtime pipeline: staged files → Files.com → compensating rollback → DB commit
* **Distinction (S16):** `ingest_excel_file()` — handles variable formatting; weakness is template dependency

---

### "Describe your ETL method for cleaning and validating data" *(AC10 — K17, S6)*

* `ingest_excel_file()` pipeline: rename → drop empties → strip prefixes → strip strings → replace absents → construct IDs → replace NaNs
* Pydantic as validation layer after Pandas transformation
* `check_lists()` — version validation, duplicate checking, error flagging before DB commit
* Legacy ETL: SQL + Pandas + Win32 → CSV seed data from SQL Server, Excel, Word

---

### "Which data engineering tools have you found most valuable?" *(AC11 — K20)*

* **Pandas** — flexible semi-structured Excel ingestion
* **SQLAlchemy ORM** — type-safe, modular, cross-engine compatible
* **Pydantic** — validation + clean user-facing error messages
* **Docker** — solved infrastructure constraint, reproducible environments
* Compared to org's existing tools: SQL Server → PostgreSQL, Excel → structured API

---

### "How do you evaluate prototype strengths and weaknesses?" *(AC12 — K24, K25, S24)*

* Supabase → Docker: identified infrastructure constraint early, adapted
* SQL Server vs PostgreSQL: evaluated Docker compatibility, constraint differences
* Custom UIDs vs integer PKs: deliberate trade-off — human-readable for non-technical staff
* Test suite as formal evaluation mechanism
* Weakness: proof-of-concept, not production-hardened; training and front-end still needed

---

### "What data quality metrics do you track?" *(AC14 — K4, S26)*

* Five dimensions: Consistency, Accuracy, Completeness, Timeliness, Validity (DAMA framework)
* KPIs: time per batch, turnaround, error rate, data accessibility
* Validation flags in API response — user-correctable before commit
* DB constraints as last-line enforcement

---

### "How do you tailor communication to different audiences?" *(AC17 — K30, S23)*

* ER diagrams → technical stakeholders; workflow diagrams → operational staff
* README + docs → developers; non-technical work instructions → centre users
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
| **Solution Architecture** | Three-tier system. ER diagram. Normalised schema, RBAC, multi-user | S3, K13, K9 |
| **ETL Pipeline** | Excel → Pandas → Pydantic → DAO → DB. Legacy ETL. Error handling flow | K17, S6, K2, S9 |
| **Security & Governance** | RBAC + magic-link tokens. SHA-256 hashing. Role permissions array. Compensating transaction in `submit()`. HTTP error hierarchy | K13, S4 |
| **Deployment & Testing** | Docker Compose. GitHub Actions CI. TDD Pytest. Proactive infrastructure fix | K6, K8, B1 |
| **Sustainability & Alignment** | Lean waste reduction. Reusable components. Org ecosystem alignment | K7, K12, S27, K26 |
| **Evaluation & Future** | Prototype decisions. Path to production. Star schema, front-end, OCR roadmap | K24, K25, K15, S24 |

---

## GAPS SUMMARY — Prioritised Report Actions

| Priority | AC | KSB | Action |
| --- | --- | --- | --- |
| 🔴 High | AC18 | S22, B2 | Add collaborative working section — who, discussions, how feedback shaped decisions |
| 🔴 High | AC17 | K30, S23 | Add communication section + distinction reflection on impact |
| 🔴 High | AC9 | K15 | Add star schema paragraph in Discussion/Recommendations |
| 🟡 Medium | AC7 | K14 | Cloud platform comparison — Supabase vs AWS vs Docker, IaaS/PaaS/SaaS |
| 🟡 Medium | AC11 | K20 | Contrast existing org tools vs new stack with justification |
| 🟡 Medium | AC13 | K26 | Add sentence on org architecture alignment |
| 🟡 Medium | AC12 | K25 | Make lifecycle journey explicit in Discussion of Findings |
| 🟢 Low | AC5 | S5 | Mention README and version-controlled docs explicitly |
| 🟢 Low | AC16 | K19 | Name structured/semi-structured/unstructured types in report |
| 🟢 Low | AC8/16 | S16 | Evaluate `ingest_excel_file()` algorithm for distinction |
| 🟢 Low | AC14 | K4 | Name DAMA framework for data quality dimensions |

---

## STILL TO BUILD — Auth Implementation Tracker

| Item | Status |
| --- | --- |
| `User` model (token_hash, role_id, centre_contact_id FK, is_active, hybrid_property display_name) | ✅ Done |
| `Role` model (role_name, permissions as ARRAY(String)) | ✅ Done |
| `db/data/roles.csv` seed file (static) | ✅ Done |
| `db/dummy_data/users.csv` seed file (test tokens as plaintext, hashed by seeder) | ✅ Done |
| `parse_pg_array()` utility in seeder — `{upload:read,upload:write}` → Python list | ⏳ To do |
| Token generation + SHA-256 hashing in seeder (`secrets` + `hashlib`) | ⏳ To do |
| `@validates('permissions')` on `Role` — array coercion (like existing boolean validators) | ⏳ To do |
| `src/auth/utils.py` — `generate_token()`, `hash_token()` | ⏳ To do |
| `src/dao/auth_dao.py` — `verify_token_and_get_user()` query | ⏳ To do |
| `src/auth/dependencies.py` — `require_permission()` FastAPI Depends | ⏳ To do |
| Apply `Depends(require_permission(...))` to upload routes | ⏳ To do |
| Tests for auth flow | ⏳ To do |

---

*Last updated: RBAC/auth design session. Topics covered: hashing concepts (bcrypt vs SHA-256), magic-link token pattern, User + Role model design, centre_contact_id as user identity anchor, permissions as PostgreSQL ARRAY, resource:action convention, FastAPI Depends() injection pattern, CSV seeding strategy for arrays and token hashes, boolean/array coercion via @validates.*
