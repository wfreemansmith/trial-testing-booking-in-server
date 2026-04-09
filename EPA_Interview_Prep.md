# EPA Interview Preparation — Wesley Freeman-Smith

## Trial Testing Booking-In Server — L5 Data Engineer

> **Revision notes** — structured around the 18 assessment criteria (ACs).
> Format per AC: example question → concept explanation → your project answer → distinction angle → follow-up questions.
> Answers reference both the written report and the codebase. Keep answers concrete and specific.

---

## How to Use This Document

- **Concept** — the underlying principle the assessor is testing
- **Your answer** — your speaking notes; adapt, don't recite verbatim
- **Distinction angle** — what lifts a pass to a distinction; always try to get this in
- **Follow-up questions** — what the assessor will probe if they want more depth

---

## DATA PRODUCT DESIGN

---

### AC1 — K9, S1, S3 | User Requirements → Scalable, Compliant Data Product

**Example question:** *How did you ensure the data product designed met both user requirements and regulatory compliance standards?*

**Concept:** Gathering user requirements means understanding what different user groups need, then translating those needs into technical decisions. Compliance means handling data in line with regulations like GDPR — appropriate access controls, data minimisation, audit trails.

**Your answer:**
I gathered requirements from three stakeholder groups: the Assessment team (what data is needed to evaluate test versions and language coverage), the Operations team (how centres submit materials and track progress through the workflow), and IT/Security (infrastructure constraints and data policies). These interviews fed directly into the data model — for example, the LanguageFamily table came from the Assessment team's need to evaluate version coverage across language groups, which wouldn't have been obvious from operational requirements alone.

I translated requirements into technical specs iteratively — the schema, API endpoints, and RBAC system were all refined through testing and stakeholder feedback. The report describes this: "early user requirements were gathered from stakeholders across the Assessment, Validation and Operations teams and translated into technical specifications... refined throughout development via testing and research."

On the compliance side, I implemented RBAC with three roles (centre_admin, staff, master) so each user accesses only what they need — the principle of least privilege. Token hashing means credentials are never stored in plaintext. The `is_active` flag allows soft-disabling users without deleting records, preserving the audit trail GDPR requires.

**Distinction angle:** Don't just say you met requirements — justify *why* specific choices met them. I chose a relational database because the data has strong referential integrity requirements — candidates belong to uploads, uploads belong to centres and windows, and FK constraints enforce this at DB level. I chose the DAO pattern because it makes the data layer independently testable. The `get_context` endpoint locks `centre_id` and `marking_window_id` to the token rather than accepting them as form data — this prevents a centre user from submitting on behalf of another centre.

**Follow-up questions to expect:**
- How did you refine requirements over time?
- How does GDPR apply specifically to your data?
- How does the `get_context` endpoint relate to compliance?

---

### AC2 — K12, S2 | Business Requirements + Sustainability / Net-Zero

**Example question:** *Describe how sustainable, net-zero technologies were considered in the design and maintenance of your data system.*

**Concept:** Sustainability in data engineering means considering the environmental cost of technology choices — energy consumption, reducing waste and redundancy, preferring cloud solutions with renewable energy commitments.

**Your answer:**
The primary sustainability argument for this project is replacing Lean waste. The existing process involves Waiting (materials sitting unprocessed), Transportation/Motion (manual file moving, email chains), and Excess Processing (duplicate data entry across spreadsheets and a SQL database that couldn't integrate with other tools). Replacing this with an automated pipeline directly reduces the energy and time cost per batch — this is stated explicitly in the scope section of the report.

At the infrastructure level, Docker means we don't run always-on dedicated hardware for development — containers are spun up when needed. The normalised database schema avoids redundant data storage compared to the existing spreadsheet approach, which duplicated information across multiple files. Reusable components (BaseDAO, shared service functions, the `api_response()` decorator) mean less code needs to be written and executed for equivalent outcomes.

**Distinction angle:** Show you evaluated options rather than just describing what you did. The choice of Docker over a managed cloud service was a deliberate trade-off — more control and on-premises compliance, at the cost of not leveraging a cloud provider's renewable energy infrastructure. That trade-off is worth naming. A future deployment on AWS (which has committed to 100% renewable energy) would be a more sustainable option.

**Follow-up questions to expect:**
- What specific Lean waste types did you reduce?
- What would a more sustainable future version of this system look like?
- How does normalisation reduce storage overhead?

---

### AC3 — K7, S27 | Sustainable Solutions, ESG, Carbon Reduction

**Example question:** *What criteria did you use to select sustainable solutions for your data product to minimise carbon footprint throughout its lifecycle?*

**Concept:** ESG (Environmental, Social, Governance) in data engineering means making technology choices that consider long-term environmental impact across the full product lifecycle.

**Your answer:**
My selection criteria were reusability, resource efficiency, and reduced redundancy across the full lifecycle.

Development: Docker means ephemeral environments — no idle compute. Reusable components (BaseDAO, shared services) reduce the amount of code that needs to be written and maintained.

Operation: Automated pipelines eliminate manual steps that would otherwise require human time and compute across multiple systems. The normalised schema stores reference data once (language families, components, versions) rather than duplicating it per record.

Deployment: Containerised builds mean the same image runs in development, testing, and production — no redundant environment-specific builds. Future managed cloud hosting (AWS, GCP) with renewable energy commitments is the next step.

End of life: Soft-delete (`is_active` flag) rather than hard delete means data is preserved without duplication — no need to re-extract from legacy sources.

**Distinction angle:** Cite the full product lifecycle explicitly. This shows you're thinking about sustainability as a design principle, not just a checkbox.

**Follow-up questions to expect:**
- What is ESG and why does it matter to Cambridge?
- How does Docker reduce carbon footprint specifically?

---

### AC4 — K13, S4 | Security, Scalability, Governance in Automated Pipelines

**Example question:** *How did you incorporate security and scalability considerations into the automation of your data pipelines?*

**Concept:** Security = only authorised users can access data, data is protected at rest and in transit. Scalability = system handles growth without rearchitecting. Governance = auditable, documented controls over who can do what.

**Your answer:**
Security is implemented at multiple layers.

**Authentication:** Magic-link tokens — a random string generated with `secrets.token_urlsafe(32)`, SHA-256 hashed before storage. The raw token is never stored; even if the database were compromised, the attacker couldn't use the hashes directly.

**Authorisation:** RBAC with three roles: centre_admin, staff, and master. Permissions stored as a PostgreSQL ARRAY on the Role model using `resource:action` convention (e.g. `upload:write`). Every route has a FastAPI dependency (`Depends(require_permission(...))`) that verifies the token, checks the role's permissions, and raises a 401 or 403 before the handler runs. The report describes this: "RBAC designed to limit access to specific resources and actions — supporting the principle of least privilege... these approaches ensure best security practices are upheld and candidate information is protected."

**Data integrity:** For cross-system operations, I implemented a compensating transaction pattern in `submit()` — because Files.com and PostgreSQL can't share a transaction boundary, I upload to Files.com first, track successes in `successful_uploads`, and roll back all external uploads if any step fails before committing to the database.

**Scalability:** Docker Compose with environment-specific volumes means scaling from development to production is a config change, not a rearchitect. The DAO pattern means the database layer is independently swappable.

**Distinction angle:** Explain *why* SHA-256 rather than bcrypt. bcrypt is correct for passwords (slow, salted, brute-force resistant) but unnecessary for random tokens where entropy is already high — `secrets.token_urlsafe(32)` produces 256 bits of entropy. SHA-256 is sufficient and faster. This shows you understand the underlying security principles, not just copied implementation. Also worth mentioning: 401 = authentication failure (who are you?), 403 = authorisation failure (what are you allowed to do?) — these are distinct and handled by the same generic HTTP exception handler using `e.status_code`.

**Follow-up questions to expect:**
- What is the difference between authentication and authorisation?
- What is a compensating transaction and when would you use one?
- What does 401 vs 403 mean?
- How would you make this system production-ready security-wise?

---

### AC5 — S5, B1 | Technical Documentation + Adapting to Changing Priorities

**Example question:** *Describe your process for producing and maintaining technical documentation for a data product, especially when facing changing work priorities.*

**Concept:** Good technical documentation is maintained alongside code, not written at the end. It serves multiple audiences — developers, operators, future maintainers.

**Your answer:**
Documentation in this project lives at several levels. Every model class, DAO method, service function, and utility has a docstring. The README covers full environment setup — Docker install, env file configuration, how to start the application. The `.env.example` files document every required configuration variable.

When priorities changed — for example when Supabase was blocked by IT Security and I had to pivot to Docker, or when I discovered the BaseDAO was causing test sessions to hang and had to refactor — both the code and documentation were updated to reflect the new approach. The report documents these decisions in the Research Outcomes section, explaining not just what was done but why.

The KSB Master List is itself a form of living documentation — mapping every technical decision to assessment criteria and version-controlled in the repo.

**Distinction angle (B1):** B1 is about proactivity and accountability. The Supabase → Docker pivot is the strongest example: I identified the blocker early (IT Security flagged it), researched alternatives, implemented Docker, and documented the decision. The report says this led to "a more production-ready architecture, reduced environment-specific issues, enabled maintainable, scalable, reproducible builds." That's a proactive response that improved the outcome.

**Follow-up questions to expect:**
- Give an example of adapting to a changing priority mid-project.
- How do you ensure documentation stays up to date?
- What would you document differently if starting again?

---

### AC6 — K6 | Debugging, Version Control, Testing

**Example question:** *How have debugging, version control, and testing principles impacted your software development processes for data products?*

**Concept:** Testing catches bugs before production. Version control enables safe iteration and rollback. Debugging systematically identifies root causes.

**Your answer:**
I used a test-driven approach throughout. The report states: "Testing was integrated from the beginning, using a Test-Driven Development approach. I used Pytest with fixtures to manage setup and teardown of environments, starting from a clean database for each test."

The test suite has six unit test files covering DAOs, utils, file handling, and the controller, plus endpoint tests covering the full upload journey from preview through to submit. Tests are parametrized against 13 different test Excel registers — covering happy paths, malformed columns, wrong formats, and duplicate candidates.

The `conftest.py` fixtures reset and reseed the database between tests, ensuring full isolation. This was critical — without it, test order would affect results.

The BaseDAO debugging is a concrete example in the report: "SQLalchemy sessions across tests caused the test runner to hang. To resolve this, I refactored my Base DAO into a context manager using Python's `__enter__` and `__exit__` methods to ensure each session was properly managed, closed and rolled back when exiting the context."

GitHub Actions runs the full test suite on every push — the report calls this "a more production-ready architecture" that it "reduced environment-specific issues." This caught environment differences between local and CI early.

For runtime debugging, `logger.py` uses Rich formatting with INFO/DEBUG level switching via a `--verbose` CLI flag — so detailed output is available when needed without polluting normal logs.

**Distinction angle:** Show cause and effect. The BaseDAO story is the strongest: the problem (sessions hanging), the debugging process (identifying session lifecycle issues), the fix (`__enter__`/`__exit__`), and what it enabled (reliable test isolation). Version control enabled the Supabase → Docker pivot without losing prior work. The commented-out `@validates` approaches in the models are evidence of iteration tracked in version history.

**Follow-up questions to expect:**
- What is a fixture and why did you use them?
- What does parametrized testing mean?
- Give a specific bug that testing caught.
- How does CI differ from CD?

---

### AC7 — K14 | Cloud Computing Platforms

**Example question:** *Explain your choice of on-demand cloud computing platforms and their impact on your data engineering projects.*

**Concept:** Cloud platforms exist on a spectrum: IaaS (raw compute/storage), PaaS (managed services), SaaS (fully managed applications). Each trades control for convenience.

**Your answer:**
The report documents the evaluation process in the Research Outcomes section. I evaluated three options for the database layer:

**Supabase** — a DBaaS (Database as a Service), PostgreSQL with a managed dashboard. Quick to set up, but IT Security blocked it because data would leave the corporate network.

**AWS SQL Server** — the Security team proposed SSH access to a shared AWS instance. However, "this solution lacked the necessary development tools (Python, Git, IDE)" — making development impractical.

**Docker with PostgreSQL** — chosen because it runs on local/internal infrastructure, gives full control over configuration, and solved the compliance requirement. The report describes this as resulting in "a more production-ready architecture, reduced environment-specific issues, enabled maintainable, scalable, reproducible builds."

For file storage, Files.com is a PaaS solution in production use — it abstracts FTP/SFTP complexity and provides API-based file management via an SDK.

**Distinction angle:** Frame this as an evaluated decision with trade-offs. Supabase rejected for compliance (data residency), AWS RDS for tooling (development environment inadequacy), Docker chosen for control and compliance. The distinction between DBaaS, IaaS, and PaaS matters — Supabase is PaaS, AWS RDS is PaaS, Docker PostgreSQL is closer to IaaS (you manage everything). Files.com is PaaS for file storage.

**Follow-up questions to expect:**
- What is the difference between IaaS, PaaS, and SaaS?
- What are the advantages of a managed cloud database?
- How would your cloud choice differ in a larger production system?

---

## DATA PRODUCT DEPLOYMENT AND EVALUATION

---

### AC8 — K8 | Deployment Approaches for Data Pipelines

**Example question:** *What deployment approaches did you use for new data pipelines and why?*

**Concept:** Deployment for data pipelines means making them consistently available across environments. This includes containerisation, CI/CD, and environment management.

**Your answer:**
The project uses Docker Compose for deployment across three environments: development, testing, and production. Each has its own configuration via `.env.{ENV}` files and its own database volume. The test runner is in a separate Docker Compose profile (`profiles: ["testing"]`) so it doesn't start in production. The report describes this leading to "consistent deployment across development, testing and production environments."

For CI/CD, GitHub Actions runs on every push. The workflow: checks out code, injects test env vars from GitHub Secrets (credentials never in the repo), builds Docker containers, runs pytest inside the container, tears everything down. CI environment is identical to local — same OS, Python version, dependencies.

For the runtime pipeline in `submit()`, the deployment approach is compensating transactions — because Files.com and PostgreSQL can't share a transaction boundary, failure at any point triggers rollback of all completed steps.

**Distinction angle (S16 — evaluate the algorithm):** For `ingest_excel_file()`:

*Strengths:* The pandas pipe chain (`rename_columns` → `drop_empty_rows` → `strip_prefixes` → `strip_strings` → `replace_absent_candidates` → `construct_version_ids` → `replace_nans`) makes each transformation step individually readable and testable. `replace_absent_candidates()` handles real-world absent markers (ABSENT, ABS, -, blank). `strip_prefixes()` handles inconsistent version naming conventions across centres.

*Weaknesses:* `header=4` is hardcoded — if the template changes row structure, the algorithm breaks silently. It's entirely template-dependent — a differently structured register would fail or produce garbage output. No OCR fallback for scanned or handwritten inputs. No confidence scoring.

*Future:* OCR (Google Cloud Vision, Tesseract) to validate scanned content. Computer vision to flag low-quality scans. Fuzzy matching for minor template deviations.

**Follow-up questions to expect:**
- What is CI and CD, and what's the difference?
- Why use Docker for testing specifically?
- What would a production deployment of this system look like?

---

### AC9 — K15 | Star Schemas, Data Lakes, Data Warehousing

**Example question:** *How have data warehousing techniques like star schemas and data lakes influenced your approach to data management?*

**Concept:** Data warehousing separates operational data (OLTP) from analytical data (OLAP). A star schema has a central fact table surrounded by dimension tables, optimised for analytical queries.

**Your answer:**
The current schema is designed for OLTP — normalised, with foreign keys and transactional integrity. This is appropriate for the operational use case: processing uploads, tracking marking progress, managing candidates. It prioritises write correctness and data integrity over read speed.

However, the Assessment and Validation team's future need is analytical — querying across windows, comparing candidate performance by language family and version, producing reports in Power BI. For this, the current schema is not optimised.

A star schema transformation would be appropriate for that future state. The fact table would be candidate results — one row per candidate per version per window, with numeric measures (writing scores, band scores). The dimension tables: Centre (centre_id, name, partner, country), Version (version_id, component, paper), Window (window_id, name, dates), Examiner, LanguageFamily. This would enable Power BI to connect directly and run analytical queries efficiently.

A data lake approach could store the raw Excel registers as uploaded — preserving unprocessed source data before transformation, useful for auditability and reprocessing if transformation logic changes.

**Distinction angle:** Show you understand *when* to use each. The current system is deliberately OLTP — that's the right choice for the operational workflow. The star schema is for a future analytical layer. These aren't competing approaches, they serve different purposes at different stages of the data lifecycle.

**Follow-up questions to expect:**
- What is the difference between OLTP and OLAP?
- What is normalisation and why does it matter?
- How would you connect Power BI to this system?

---

### AC10 — K17, S6 | ETL — Clean, Validate, Combine Disparate Sources

**Example question:** *Describe your method for systematically cleaning and validating data throughout the ETL process.*

**Concept:** ETL (Extract, Transform, Load) takes data from source systems, transforms it into a usable format, and loads it into the target. Each stage requires quality checks.

**Your answer:**
There are two distinct ETL processes in this project.

**Legacy ETL (seeding):** Extracting from the legacy SQL Server database using raw SQL. `select_centre_contacts.sql` is the most complex — the legacy database stored multiple contacts per centre in separate columns (`ContactName1`, `ContactEmail1`, `ContactName2`, `ContactEmail2`) with semicolon-delimited emails. I used a CTE with `UNION ALL` to unpivot these into rows, then `CROSS APPLY STRING_SPLIT` to split the semicolons, then `ROW_NUMBER()` to assign `primary_contact`. The report describes this: "I used a combination of SQL queries and Python libraries (Pandas, Win32) to prepare CSV-formatted seed data."

**Runtime ETL (register ingestion):** When a centre uploads an Excel register, `ingest_excel_file()` processes it through a pandas pipe chain: rename columns to standardised names, drop empty rows, strip version prefixes (ACW, GTR, etc.), strip whitespace, replace absent candidate markers (ABSENT, ABS, -, blank) with None, construct version IDs, replace NaN with None. The output feeds into Pydantic validation, then into `check_lists()` which validates against the database.

Errors are returned to the user in the API response with field-level error messages — users can correct their data before final submission. The report states: "The system differentiates between expected user errors (such as missing fields, duplicate candidates, incorrect formats) and system errors (database failures, exceptions), providing clear and actionable feedback."

**Distinction angle:** The layered validation approach is worth explaining explicitly: Pandas handles structural transformation, Pydantic handles type and format validation, `check_lists()` handles business rule validation (duplicates, version existence, future test dates), and database constraints are the final layer. Each layer catches different problems at the appropriate stage, for the appropriate audience.

**Follow-up questions to expect:**
- What is the difference between transformation and validation?
- How did you handle missing or malformed data?
- What does idempotent mean in ETL context?

---

### AC11 — K20 | Data Engineering Tools

**Example question:** *Which data engineering tools have you found most valuable in your work, and how do you apply them?*

**Concept:** A data engineer should understand their tool landscape — what each tool does, why you'd choose it over alternatives, how they fit together.

**Your answer:**
The existing tools at Cambridge are SQL Server (database), Excel (end-user data), and Power BI (reporting). These are fit-for-purpose for their existing roles but don't support an automated pipeline.

My new stack and why each was chosen:

**FastAPI** — native async support, automatic OpenAPI docs, `Depends()` injection system made auth clean to implement. The report describes the backend design: "FastAPI and followed a loosely structured MVC pattern... modular approach made the codebase easier to navigate, test and build upon."

**SQLAlchemy ORM** — makes the data layer independently testable, cross-engine compatible. The report: "investing time in defining models with referential integrity and building a DAO layer to keep logic modular and testable."

**Pandas** — handles semi-structured tabular data flexibly. The pipe chain pattern makes transformation steps readable and individually testable. Report: "Pandas for extraction and transformation."

**Pydantic** — input validation, schema definition, `model_dump()` for clean DAO handoff. Report: "paired with Pydantic schemas to validate input and enforce consistency."

**Docker** — solved the infrastructure reproducibility problem. Same environment in development, testing, and CI.

**pyodbc** — connects to the legacy SQL Server database using Windows Authentication. Bridges old and new stack without requiring credential management.

**Distinction angle:** Explain trade-offs, not just what you used. Why Pandas over openpyxl? Pandas provides DataFrame transformations and the pipe chain; openpyxl is for cell-level manipulation. Why SQLAlchemy over raw SQL? Modularity and testability. Why Pydantic over manual validation? Type coercion, user-facing error messages, and serialisation.

**Follow-up questions to expect:**
- What is an ORM and what are its advantages and disadvantages?
- Why would you ever use raw SQL over an ORM?
- What is pyodbc and what does Windows Authentication mean?

---

### AC12 — K24, K25, S24 | Prototype Evaluation + Solution Lifecycle

**Example question:** *How do you evaluate the strengths and weaknesses of prototype data products within your organisation's data architecture?*

**Concept:** Prototyping is about building to learn — identifying what works, what doesn't, and what the constraints are before committing to production. The lifecycle spans scoping, prototyping, development, production, and continuous improvement.

**Your answer:**
The lifecycle for this project: Planning (stakeholder interviews, requirements gathering), Design (schema design, API design), Development (current phase — building and testing the backend), followed by planned Consultation, Training, Deployment, and Maintenance.

Key prototype decisions and how they were evaluated:

**Database infrastructure:** Started with Supabase, blocked by IT Security, pivoted to Docker. The report describes this as resulting in "a more production-ready architecture" — the constraint forced a better outcome.

**Primary key strategy:** Evaluated auto-increment integers vs composite string UIDs. Chose composite UIDs (`{window_id}_{centre_id}_{part_delivery}`) because they're human-readable for non-technical staff who might query the database directly. The commented-out `@validates`-based generation approach in the models shows iteration — it was found to be unreliable and replaced with `__init__`-based generation.

**ORM approach:** SQL Server vs PostgreSQL (chose PostgreSQL for Docker compatibility and constraint support). Raw SQL vs ORM (chose ORM for testability).

**RBAC design:** Dynamic URL-based permission derivation was evaluated and rejected — explicit `resource:action` strings are more maintainable and auditable.

Current prototype's known weaknesses: no frontend (proof-of-concept only), auth seeder not yet implemented, not production-hardened (no rate limiting, no audit logging, no monitoring).

**Distinction angle (S24):** Evaluate integration with the *organisation's* data architecture specifically. The system feeds into Power BI (via normalised schema → future star schema), integrates with legacy SQL Server (pyodbc for seed data), and aligns with Files.com infrastructure already in use. It doesn't replace existing systems — it orchestrates them.

**Follow-up questions to expect:**
- What would you need to do to take this from prototype to production?
- What are the risks of deploying this as-is?
- How did stakeholder feedback change the design?

---

### AC13 — K26 | Organisational Architectures and Frameworks

**Example question:** *How do you align your data development projects with approved organisational architectures?*

**Concept:** Organisations have approved technology stacks, coding standards, and architectural patterns. Good data engineers work within these constraints.

**Your answer:**
Cambridge uses a relational database stack (SQL Server) and Power BI for reporting. My project uses PostgreSQL — a different engine, but the same relational paradigm — which means the data model and query patterns are familiar and future Power BI integration is straightforward. I aligned with this preference rather than proposing a document store or NoSQL approach. The scoping document states: "following the organisation's preference for relational databases."

The use of pyodbc for the legacy SQL Server connection ensures the new system can interoperate with existing infrastructure. The CSV seed data format was chosen to be readable and editable by operations staff familiar with Excel.

I followed Python coding standards (PEP 8) throughout and used a layered MVC-adjacent architecture (routes, controllers, services, DAOs, models) which is a recognised, maintainable pattern.

**Distinction angle:** Show you understand why the organisation made its choices. SQL Server + Power BI is a Microsoft ecosystem choice — it integrates with other Microsoft tools, reduces training overhead and support costs. Working within that ecosystem was a deliberate design constraint, not a limitation.

**Follow-up questions to expect:**
- What is PEP 8?
- Why would an organisation standardise on a particular technology stack?
- How would you handle a situation where the approved architecture isn't the best technical choice?

---

### AC14 — K4, S26 | Data Quality Metrics

**Example question:** *What process do you follow to identify and track data quality metrics for ensuring accuracy and reliability?*

**Concept:** The DAMA framework defines five data quality dimensions: Accuracy, Completeness, Consistency, Timeliness, and Validity.

**Your answer:**
My five quality dimensions map directly to the DAMA framework:

**Accuracy** — `validate_candidate()` checks required fields are present and correctly formatted. Database FK constraints ensure candidates belong to valid uploads, uploads to valid centres. `CheckConstraint` on `centre_id` enforces the four-digit numeric format.

**Completeness** — `check_lists()` flags missing candidate names, numbers, and paper type. Empty rows are dropped in the Pandas pipeline before any validation occurs.

**Consistency** — `is_duplicate_candidate()` checks incoming candidates against the database to prevent the same candidate appearing twice across uploads. In-list duplicates are also detected. It uses a three-case logic: full duplicate (True), number-only duplicate (returns next available number), new candidate (False) — using `itertools.chain` to find the max number across both the incoming list and existing database records.

**Timeliness** — `check_lists()` validates that `test_date` is not in the future. The marking window expiry check in the auth dependency ensures submissions only occur within the valid window (plus 7-day grace period).

**Validity** — version IDs are validated against the database via `validate_version()`. File uploads are checked for correct MIME type and extension at the route level.

Errors are returned to the user with field-level messages — quality issues are surfaced for correction rather than silently dropped. The report states: "The system differentiates between expected user errors (such as missing fields, duplicate candidates, incorrect formats) and system errors."

**Distinction angle:** The layered enforcement approach: Pandas (structural), Pydantic (type/format), `check_lists()` (business rules), DB constraints (last line). Each layer has a different audience — Pandas errors go to developers, Pydantic errors to API consumers, business rule errors to end users as actionable field-level messages, DB constraints should never be reached if earlier layers work.

**Follow-up questions to expect:**
- What is the DAMA framework?
- How would you track data quality over time, not just at ingestion?
- What is referential integrity?

---

### AC15 — K2, S9 | Query, Manipulate, Move Data Between Systems

**Example question:** *Discuss the methodologies you've used for moving and handling data across systems, emphasising query and manipulation techniques.*

**Concept:** Data engineering involves moving data between systems — extracting from sources, transforming in transit, loading into targets. Requires both query skills (SQL, ORM) and manipulation skills (Python, Pandas).

**Your answer:**
There are three distinct data movement patterns:

**Legacy extraction (SQL → CSV):** Raw SQL queries against SQL Server using pyodbc. `select_centre_contacts.sql` uses CTEs, `UNION ALL`, `CROSS APPLY STRING_SPLIT`, `ROW_NUMBER()` — extracting normalised contact data from a denormalised legacy schema. Output is CSV files used to seed the new database. The report: "I used a combination of SQL queries and Python libraries (Pandas, Win32) to prepare CSV-formatted seed data."

**Runtime ingestion (Excel → PostgreSQL):** The `ingest_excel_file()` pandas pipeline transforms semi-structured Excel into clean Python objects. Pydantic validates. `UploadDAO.create_upload_object()` builds the nested object graph (Upload → Batches → Candidates → FileUploads) and commits in a single transaction.

**File movement (filesystem → Files.com → PostgreSQL):** `submit()` moves PDF files from local temp directory to Files.com via the SDK, then records the upload in PostgreSQL. Compensating transaction pattern ensures consistency.

The BaseDAO provides a reusable query interface — `select(**kwargs)` builds dynamic AND conditions using SQLAlchemy's `and_()`, so any DAO can query by any combination of model attributes without writing raw SQL. `is_duplicate_candidate()` uses `itertools.chain` to find the maximum candidate number across both incoming list and database results in a single pass.

**Distinction angle:** The methodology distinction is the separation of concerns — SQL for structured legacy queries, Pandas for semi-structured transformation, SQLAlchemy ORM for transactional DB operations, Files.com SDK for binary file movement. Each tool chosen for the job it's best at.

**Follow-up questions to expect:**
- What is an ORM query vs a raw SQL query?
- How does a transaction work?
- What does atomicity mean?

---

### AC16 — K19, S16 | Structured, Semi-Structured, Unstructured Data

**Example question:** *How have you adapted your strategies to work with structured, semi-structured, and unstructured data?*

**Concept:** Structured data has a fixed schema (SQL tables). Semi-structured has flexible/inconsistent schema (Excel, JSON, CSV with variability). Unstructured has no schema (PDFs, images, free text).

**Your answer:**
All three types appear in this project. The report's ETL section describes: "sources included our relational database (SQL Server), Excel workbooks, Word documents, and text-based extracts."

**Structured:** The legacy SQL Server database — fixed schema, typed columns. Queried with raw SQL and loaded into CSV for seeding.

**Semi-structured:** The candidate Excel registers — they follow a template, but centres introduce variations (extra columns, inconsistent version naming prefixes like ACW vs ACR vs List, absent markers like ABSENT/ABS/-). `ingest_excel_file()` handles this variability — stripping prefixes, replacing absent markers, dropping empty rows — before converting to a structured format. The legacy `select_centre_contacts.sql` also handles semi-structured input: semicolon-delimited emails and multi-column contact data.

**Unstructured:** PDF scans of candidate answer sheets. The system stages and uploads them as binary files via Files.com, linked to the relevant batch. Content parsing would require OCR (noted as a future enhancement in the scoping document).

**Distinction angle (S16):** Evaluate `ingest_excel_file()` honestly.

*Strengths:* Pandas pipe chain makes each step readable and testable individually. `replace_absent_candidates()` handles real-world markers centres actually use. `strip_prefixes()` handles inconsistent naming. `warnings.filterwarnings` suppresses a known openpyxl warning.

*Weaknesses:* `header=4` is hardcoded — if the template changes row structure, the algorithm breaks. Template-dependent — won't work with a differently structured register. No confidence scoring or OCR fallback.

*Future:* OCR (Google Cloud Vision, Tesseract) for scanned content. Computer vision to flag low-quality scans. Fuzzy matching for minor template deviations. The scoping document explicitly mentions OCR and CV as potential future features.

**Follow-up questions to expect:**
- What is OCR and where would it fit in this pipeline?
- How would you handle a completely unknown file format?
- What is schema inference?

---

## COLLABORATIVE WORKING

---

### AC17 — K30, S23 | Communicating About the Data Product

**Example question:** *How do you tailor your communication strategies to effectively convey data product messages to diverse audiences?*

**Concept:** Different audiences need different types of information — technical teams need architecture and implementation detail; operational teams need process and workflow; end users need simple, actionable instructions.

**Your answer:**
I identified four distinct audiences and tailored communication accordingly:

**IT/Security:** Technical architecture — data flow, security model, compliance with data policies. The conversation about Supabase being blocked led directly to the Docker decision. Communication via technical documentation and meetings.

**Assessment/Validation team:** Data model and query capability — ER diagrams showing how candidate data, versions, and language families relate. They needed to understand what analytical queries would be possible once live. This conversation led to LanguageFamily being included in the schema.

**Operations team:** Process diagrams — how the current manual workflow maps to the new automated one, what changes per role, what stays the same. Non-technical language, focused on outcomes rather than implementation.

**Centre contacts (end users):** Simple work instructions — how to fill in the register template, how to upload, what error messages mean and how to fix them. The `api_response()` envelope with `{status, message, data}` was designed to be frontend-friendly and human-readable.

The README and `.env.example` files serve the developer audience — step-by-step setup, no assumed knowledge beyond Docker basics.

**Distinction angle:** Evaluate the *impact* of communication — what changed as a result? The IT/Security conversation changed the infrastructure approach entirely (Supabase → Docker). The Assessment team's requirement for language family data led to that being included in the schema when it wouldn't have been obvious from operational requirements alone. Communication wasn't just informational — it shaped the product.

**Follow-up questions to expect:**
- How did you decide what level of detail to include for each audience?
- Give an example of where communication directly influenced a technical decision.
- How would you communicate a technical limitation to a non-technical stakeholder?

---

### AC18 — S22, B2 | Collaborative Working with Stakeholders

**Example question:** *Describe a collaborative project where you developed and maintained effective working relationships with different stakeholders.*

**Concept:** Collaborative working means actively involving stakeholders throughout — not just requirements at the start and a presentation at the end, but ongoing dialogue, incorporating feedback, and adapting as understanding develops.

**Your answer:**
This project required collaboration across four groups:

**Assessment team:** Provided data requirements for versions, language families, and answer keys. Their input shaped the Version, AnswerKey, and LanguageFamily tables. I met with them early to understand what analytical output needed to look like, then fed this back into the schema design.

**Operations team:** Provided workflow requirements — how centres submit materials, how batches are assigned to examiners, how marking progresses. The Upload → Batch → Candidate structure directly reflects their operational process.

**IT/Security:** The most consequential collaboration. When I proposed Supabase, IT Security flagged data residency concerns. Rather than treating this as obstruction, I treated it as a legitimate requirement — the Docker solution that resulted is more secure and controllable. This is described in the report's Research Outcomes.

**My manager:** Provided ongoing sign-off and resource allocation. Regular progress updates meant no surprises, and feedback was incorporated incrementally.

I adapted communication style for each group — technical documentation for IT, process diagrams for Operations, data model discussions for Assessment. I actively sought constructive criticism rather than presenting finished designs for approval.

**Distinction angle (B2):** The distinction for B2 is about *how* you collaborated — inclusive culture, treating technical and non-technical colleagues with respect. The IT Security interaction is the key example: treating the compliance constraint as a legitimate requirement and working with them rather than around them led to a better technical outcome and a stronger working relationship.

**Follow-up questions to expect:**
- How did you handle disagreement with a stakeholder?
- How did you keep stakeholders informed of progress?
- Give an example of where stakeholder feedback improved the technical design.

---

## DISTINCTION CRITERIA — Quick Reference

| AC | Distinction Requirement | Your Evidence |
| --- | --- | --- |
| AC1 (S1, S3) | Justify *why* the product met requirements and served multiple needs | Relational DB for referential integrity; DAO for testability; RBAC for least privilege; `get_context` prevents data tampering |
| AC8 (S16) | Evaluate the success of the algorithm developed | `ingest_excel_file()` — strengths: pipe chain, absent markers; weaknesses: `header=4` hardcoded, template-dependent; future: OCR |
| AC17 (K30, S23) | Evaluate the *impact* of communication methods | IT/Security conversation → Docker decision; Assessment input → LanguageFamily in schema |

---

## KEY CONCEPTS QUICK REFERENCE

| Term | Plain English |
| --- | --- |
| RBAC | Role-Based Access Control — users get permissions based on their role, not individually |
| Compensating transaction | When two systems can't share a transaction, undo completed steps if any step fails |
| SHA-256 | Fast one-way hash — good for tokens; use bcrypt for passwords (slower, salted) |
| Magic link | Auth via a link with a token in the URL — no password needed |
| DAMA framework | Five data quality dimensions: Accuracy, Completeness, Consistency, Timeliness, Validity |
| OLTP vs OLAP | OLTP = transactional (writes, operational); OLAP = analytical (reads, aggregations) |
| Star schema | Fact table surrounded by dimension tables — optimised for analytical queries |
| ETL | Extract, Transform, Load — the process of moving data between systems |
| DAO | Data Access Object — a class that encapsulates database queries for a model |
| IaaS / PaaS / SaaS | Infrastructure / Platform / Software as a Service — increasing levels of managed abstraction |
| Normalisation | Designing a DB to reduce redundancy by separating data into related tables |
| Parametrized test | A single test function run with multiple input/output combinations |
| Fixture | Test setup/teardown code that runs before/after tests |
| Pipe chain | Chaining pandas transformations: `df.pipe(f1).pipe(f2).pipe(f3)` |
| Least privilege | Users/processes have only the permissions they need — no more |
| 401 vs 403 | 401 = not authenticated (who are you?); 403 = not authorised (what are you allowed to do?) |
| Compensating transaction | When two systems can't share a transaction, track successes and roll back if any step fails |

---

*Last updated: essay content reviewed and incorporated into project answers. Report status confirmed — four sections (Data Product Outcomes, Project Outcomes, Discussion, Recommendations) still to be written. All answers updated to reference specific report sections where written.*
