# Trial Testing Booking in Server

## Environment Setup & Configuration

This project uses Docker Compose to run the application services, including the PostgreSQL database, server, and test runner. Configuration is managed via environment variables to support multiple deployment environments such as **development** and **production**.

Environment variables are stored in `.env` files for each environment:
  - `.env` — base variables to set the environment
  - `.env.development` — variables specific to the development environment
  - `.env.production` — variables specific to the production environment
  - `.env.testing` variables specific to the testing environment
  
  The `APP_ENV` variable controls which environment config is active and is set in the `.env` file. Once this has been set, volumes and all other environmental variables are set dynamically.

## Getting Started

Follow these steps to set up and run the project locally using Docker Compose:

1. **Install Docker & Docker Compose**

   If you don’t have Docker and Docker Compose installed, follow the official installation guide here:  
   [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

2. **Clone this repository**
   
   Run the following:
   ```bash
   git clone https://github.com/ielts-ops/trial-testing-booking-in-server.git
   cd trial-testing-booking-in-server
   ```

3. **Create and configure environment files**

    Copy the example environment files to your working directory by running:
    ```bash
    cp .env.example .env
    cp .env.name.example .env.development
    cp .env.name.example .env.testing
    cp .env.name.example .env.production
    ```

    Edit each .env* file to set the appropriate environment variables such as database credentials, ports, and APP_ENV.
    
    Make sure .env contains the APP_ENV variable, for example:
    ```bash**
    APP_ENV=development
    ```

4. **Start the application**

    Run Docker Compose to build and start all containers by running:
    ```
    docker-compose up --build
    ```

    This will start the database, server, and test containers configured for the environment specified in your .env file.

5. **Access the application**

    Once running, your server should be accessible on http://localhost:8000 (or the port defined in your .env files).

## Data Quality Metrics

This project applies the six DAMA data quality metrics across the pipeline. 

1. **Completeness**

    Records are fully populated with required information by explicity stating `nullable=False` at the database level:
    ```python
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    centre_contact_id = Column(Integer, ForeignKey("centre_contacts.centre_contact_id"), nullable=True)
    ```
    Empty rows are dropped by Pandas at ingestion stage, and functions like `validate_candidates()` flag missing fields before commit:
    ```python
    if not candidate.candidate_name:
        candidate.errors.append(
            ErrorMessage(field="candidate_name", message="Candidate name cannot be blank. Please provide a name for the candidate.")
        )
    ```

2. **Uniqueness**

    Unique fields in the database are constrained by the `unique=True` option. Ingestion logic in `CandidateDao()` checks against existing records for duplicates, returning a boolean mask:
    ```python
    list_to_return = []
    for candidate in candidate_list:
        duplicate = any(
            entry.candidate_number == candidate[0] and entry.candidate_name == candidate[1]
            for entry in existing_candidates
        ):
        # ...
        list_to_return.append(duplicate)
    ```

3. **Consistency**

    Pydantic schema enforce uniform data contracts across all boundaries:
    ```python
    class UploadData(BaseModel):
        epd_number: Optional[str] = None
        test_date: Optional[date] = None
        batches: List[BatchDict]
        candidates: List[CandidateDict]

    def parse_upload_data(data: dict) -> UploadData:
        return UploadData(**data)
    ```
    Cross-system, `construct_upload_filename()` and `construct_upload_path()` enforce agreed naming conventions:
    ```python
    return f"{centre_id}_{version_id}_{str(lowest_cand).zfill(4)}-{str(highest_cand).zfill(4)}_{num_of_cands} candidates"
    ```
    At system boundaries, a compensating transaction pattern is implemented in `submit()`:
    ```python
    except Exception as e:
        logger.error(f"Upload failed, attempt rollback of {len(successful_uploads)} files")
        for staged in successful_uploads:
            file_handler.delete_file(staged.destination_folder, staged.destination_filename)
        raise
    ```

4. **Accuracy**
    Foreign key constraints ensure every candidate, batch and upload record relates to a valid existing parent record:
    ```python
    class CentreContact(Base):
        __tablename__ = "centre_contacts"
        centre_id = Column(String(4), ForeignKey("centres.centre_id"), nullable=False)
        # ...
        centre = relationship("Centre", back_populates="contacts")
    ```
    `CheckConstraint` in the `centre` table ensures all centre records are maintained correctly:
    ```python
    centre_id = Column(String(4), CheckConstraint("centre_id ~ '^[0-9]{4}$'", name="centre_id_check"), primary_key=True)
    ```

5. **Timeliness**

    Checks validity in the `auth` dependency, rejecting data submitted outside of valid operational windows:
    ```python
    def require_centre_permission(action: str) -> User:
        def dependency(q: str = Query(...), db: Session = Depends(get_db)):
            user = verify_token_get_user(q, db)
            # ...
            if user.marking_window and date.today() > (user.marking_window.window_end  + timedelta(days=7)):
                raise HTTPException(status_code=403, detail="Marking window has closed")
            # ...
            return user
            
        return dependency
    ```
    Upload date set in `class Upload()` so timestamps are recored at ingestiong, providing auditable record:
    ```python
    upload_date = Column(Date, server_default=func.now())
    ```

6. **Validity**
    
    Routes check for valid file types before progressing further:
    ```python
    if file.filename.endswith('.xlsx'):
        file_bytes = await file.read()
    else:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type .{file.filename.split(".")[-1]} not supported"
        )
    ```
    Incoming data is validated against the database, for example `validate_version()`:
    ```python
    with get_db_session() as session:
        dao = VersionDAO(session)
        version_exists = dao.version_exists(batch.version_id)
    
    if not version_exists:
        batch.errors.append(
            ErrorMessage(field="batches", message=f"...")
        )
    ```