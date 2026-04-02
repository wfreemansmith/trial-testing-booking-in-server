from sqlalchemy import Column, Integer, Numeric, Float, String, Text, Date, Boolean, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, validates, declarative_base, reconstructor
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import ARRAY
import hashlib


Base = declarative_base()

class User(Base):
    """User table for staff, centres and master"""
    __tablename__ = "users"

    # generated fields
    user_id = Column(Integer, primary_key=True, autoincrement=True)

    # provided fields
    token_hash = Column(String, nullable=False, unique=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    centre_contact_id = Column(Integer, ForeignKey("centre_contacts.centre_contact_id"), nullable=True)
    marking_window_id = Column(Integer, ForeignKey("marking_windows.marking_window_id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(Date, server_default=func.now())
    
    # relationships
    role = relationship("Role", back_populates="users")
    centre_contact = relationship("CentreContact", back_populates="user", uselist=False)
    marking_window = relationship("MarkingWindow", back_populates="users")

    @hybrid_property
    def display_name(self) -> str:
        if self.centre_contact:
            return self.centre_contact.contact_name
        return "Admin"
    
    @validates
    def hash_token(self, key, value):
        if len(value) == 64:
            return value
        return hashlib.sha256(value.encode()).hexdigest()


class Role(Base):
    """Roles and access levels"""
    __tablename__ = "roles"

    # generated field
    role_id = Column(Integer, primary_key=True, autoincrement=True)

    # provided fields
    role_name = Column(String, nullable=False, unique=True)
    permissions = Column(ARRAY(String), nullable=False, default=[])

    # relationships
    users = relationship("User", back_populates="role")

    @validates('permissions')
    def parse_array(self, key, value):
        """
        Parses array strings e.g.
        '{upload:read},{upload:write}' -> ['upload:read', 'upload:write']
        """
        if isinstance(value, list):
            return value
        return [p.strip("{ }").lower() for p in value.split(",")]
    

class CandidateFeedback(Base):
    """Reference table for pre-written feedback offered to candidates upon return of their results. Feedback is organised by bandscore and by component"""
    __tablename__ = "candidate_feedback"

    # provided fields
    bandscore = Column(String(50), primary_key=True)
    listening_feedback = Column(Text)
    reading_feedback = Column(Text)
    writing_feedback = Column(Text)


class ExaminerPaymentRate(Base):
    """Examiner payments rates differ depending on their location, currency, and what component / item they've completed. Pay is per item (e.g. per report, per script)
    Rate IDs and other details need to match those found on our Rates Management System."""
    __tablename__ = "examiner_payment_rates"

    # provided fields
    rate_id = Column(Integer, primary_key=True)
    location = Column(String(50))
    currency = Column(String(3))
    component = Column(String(2))
    item = Column(String(50))
    rate = Column(Numeric(10,2))
    unit = Column(String(10))
    holiday_rate = Column(Float)


class MarkingWindow(Base):
    """A marking window is a period of time during which partipating centres can conduct trial tests.
    Also referred to as 'Sessions', however changed for the database to distinguish from SQLalchemy Sessions."""
    __tablename__ = "marking_windows"

    # generated fields
    marking_window_id = Column(Integer, primary_key=True, autoincrement=True)
    # provided fields
    window_name = Column(String(50), nullable=False)
    window_start = Column(Date, nullable=False)
    window_end = Column(Date, nullable=False)
    window_upload_destination = Column(String)

    # relationships
    uploads = relationship("Upload", back_populates="marking_window")
    requests = relationship("CentreRequests", back_populates="marking_window", cascade="all, delete-orphan")
    user = relationship("User", back_populates="marking_window")


class LanguageFamily(Base):
    """Reference table for language families, by country or by language.
    Language family is an important concept in Trial Testing, as we will use this data to assess whether a version has been broadly tested enough."""
    __tablename__ = "language_families"
    
    # generated fields
    language_fam_id = Column(Integer, primary_key=True, autoincrement=True)
    # provided fields
    language_family = Column(String, nullable=False)

    # relationships
    countries = relationship("Country", back_populates="language_family")
    languages = relationship("Language", back_populates="language_family")


class Country(Base):
    """Representing countries that Centres are based in. Each country belongs to a LanguageFamily."""
    __tablename__ = "countries"
    
    # provided fields
    country_id = Column(Integer, primary_key=True)
    country = Column(String, nullable=False)
    language_fam_id = Column(Integer, ForeignKey("language_families.language_fam_id"))

    # relationships
    language_family = relationship("LanguageFamily", back_populates="countries")
    centres = relationship("Centre", back_populates="country")


class Language(Base):
    """Representing the first language reported by Candidates. Languages belong to LanguageFamilies."""
    __tablename__ = "languages"

    # provided fields
    language_id = Column(Integer, primary_key=True)
    language = Column(String, nullable=False)
    language_fam_id = Column(Integer, ForeignKey("language_families.language_fam_id"))

    # relationships
    language_family = relationship("LanguageFamily", back_populates="languages")
    candidates = relationship("Candidate", back_populates="language")


class Centre(Base):
    """Main table for registered Trial Test Centres"""
    __tablename__ = "centres"

    # provided fields
    centre_id = Column(String(4), CheckConstraint("centre_id ~ '^[0-9]{4}$'", name="centre_id_check"), primary_key=True)
    live_centre_number = Column(String)
    centre_name = Column(String, nullable=False)
    partner = Column(String, nullable=False)
    address_1 = Column(String)
    address_2 = Column(String)
    address_3 = Column(String)
    address_4 = Column(String)
    address_5 = Column(String)
    tax_id = Column(String)
    country_id = Column(Integer, ForeignKey("countries.country_id"))
    phone_number = Column(String)

    # relationships
    country = relationship("Country", back_populates="centres")
    contacts = relationship("CentreContact", back_populates="centre", cascade="all, delete-orphan")
    uploads = relationship("Upload", back_populates="centre")
    requests = relationship("CentreRequests", back_populates="centre", cascade="all, delete-orphan")


class CentreContact(Base):
    """Each entry represents one contact at a Trial Testing Centre. Each centre can have many contacts."""
    __tablename__ = "centre_contacts"

    # generated fields
    centre_contact_id = Column(Integer, primary_key=True, autoincrement=True)
    # provided fields
    centre_id = Column(String(4), ForeignKey("centres.centre_id"), nullable=False)
    contact_name = Column(String, nullable=False)
    contact_email = Column(String, nullable=False)
    primary_contact = Column(Boolean, default=False)

    # relationships
    centre = relationship("Centre", back_populates="contacts")
    user = relationship("User", back_populates="centre_contact")

    # validation
    @validates('primary_contact')
    def convert_to_boolean(self, key, value):
        if isinstance(value, str):
            return value.strip().lower() in ('true', '1', 'yes', 'y')
        return bool(value)


class CentreRequests(Base):
    """Contains all centre requests by marking window. Used to create upload folders, share links, etc."""
    __tablename__ = "centre_requests"

    # generated fields
    request_id = Column(Integer, primary_key=True, autoincrement=True)
    # provided fields
    marking_window_id = Column(Integer, ForeignKey("marking_windows.marking_window_id"))
    centre_id = Column(String(4), ForeignKey("centres.centre_id"), nullable=False)
    acw_requests = Column(Integer)
    acr_requests = Column(Integer)
    gtw_requests = Column(Integer)
    gtr_requests = Column(Integer)

    # relationships
    marking_window = relationship("MarkingWindow", back_populates="requests")
    centre = relationship("Centre", back_populates="requests")


class ExaminerRole(Base):
    """Reference table for different types of examiner, e.g. TTE, APE, PE"""
    __tablename__ = "examiner_roles"

    # generated fields
    examiner_role_id = Column(Integer, primary_key=True, autoincrement=True)
    # provided fields
    examiner_role = Column(String, nullable=False)

    # relationships
    examiners = relationship("Examiner", back_populates="examiner_role")


class Examiner(Base):
    """Table containing all examiners details, including their personal details, country, as_id and role"""
    __tablename__ = "examiners"

    # provided fields
    examiner_id = Column(Integer, primary_key=True) # use AS ID
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    contact_email = Column(String, nullable=False)
    # as_id = Column(Integer, nullable=False)
    country = Column(String)
    currency = Column(String)
    examiner_role_id = Column(Integer, ForeignKey("examiner_roles.examiner_role_id"))
    last_contract_signed = Column(String)
    active = Column(Boolean, default=True)

    # relationships
    examiner_role = relationship("ExaminerRole", back_populates="examiners")
    availability = relationship("ExaminerAvailability", back_populates="examiner")
    batches = relationship("Batch", back_populates="examiner")
    reports = relationship("VersionReport", back_populates="examiner")

    # validation
    @validates('active')
    def convert_to_boolean(self, key, value):
        if isinstance(value, str):
            return value.strip().lower() in ('true', '1', 'yes', 'y')
        return bool(value)


class ExaminerAvailability(Base):
    """For examiners to provide their weekly availability. Not linked to marking windows, just week beginning dates. Used to determine who is available to mark a batch."""
    __tablename__ = "examiner_availability"

    # generated fields
    week_id = Column(Integer, primary_key=True, autoincrement=True)
    # provided fields
    examiner_id = Column(Integer, ForeignKey("examiners.examiner_id"), nullable=False)
    week_beginning = Column(Date, nullable=False)
    week_ending = Column(Date, nullable=False)
    script_availability = Column(Integer, default=0)
    remaining_scripts = Column(Integer, default=0)

    # relationships
    examiner = relationship("Examiner", back_populates="availability")
    

class Component(Base):
    """Reference table for Academic and General Training components"""
    __tablename__ = "components"

    # provided fields
    component_id = Column(String(1), primary_key=True)
    description = Column(String)

    # relationships
    versions = relationship("Version", back_populates="component")
    batches = relationship("Batch", back_populates="component")


class Version(Base):
    """Contains all Trial Testing Exam Versions"""
    __tablename__ = "versions"

    # generated fields
    version_id = Column(String, primary_key=True)
    # provided fields
    paper = Column(String(2), default="")
    component_id = Column(String(1), ForeignKey('components.component_id'), nullable=False)
    version_name = Column(String, nullable=False)

    # relationships
    component = relationship("Component", back_populates="versions")
    answer_key = relationship("AnswerKey", back_populates="version")
    # candidates = relationship("Candidate", back_populates="version")
    reports = relationship("VersionReport", back_populates="version")
    cwas = relationship("CommonWrongAnswer", back_populates="version")
    batches = relationship("Batch", back_populates="version")
    responses = relationship("CandidateResponse", back_populates="version")

    @validates('paper', 'component_id', 'version_name')
    def generate_id(self, key, value):
        paper = value if key == 'paper' else self.paper
        if paper not in ("", "AC", "GT"):
            raise ValueError(f"Invalid paper value: {paper}")
        
        component_id = value if key == 'component_id' else self.component_id
        version_name = value if key == 'version_name' else self.version_name
        
        if paper is not None and component_id is not None and version_name is not None:
            self.version_id = f"{paper}{component_id}{version_name}"
        
        return value


class VersionReport(Base):
    """Table for managing writing reports, completed by examiners following a version pass"""
    __tablename__ = "version_reports"

     # provided fields
    report_id = Column(Integer, primary_key=True)
    version_id = Column(String, ForeignKey("versions.version_id"), nullable=False)
    examiner_id = Column(Integer, ForeignKey("examiners.examiner_id"))
    date_requested = Column(Date)
    deadline_date = Column(Date)
    date_returned = Column(Date)

    # relationships
    version = relationship("Version", back_populates="reports")
    examiner = relationship("Examiner", back_populates="reports")


class AnswerKey(Base):
    """Answer keys for Reading & Listening versions. Can compare CandidateResponses to answers in this table for auto-marking."""
    __tablename__ = "answer_keys"

    # generated fields
    answer_id = Column(String, primary_key=True)
    # provided fields
    version_id = Column(String, ForeignKey("versions.version_id"), nullable=False)
    question_number = Column(Integer, nullable=False)
    answer = Column(String, nullable=False)
    productive_answer = Column(Boolean, default=False)
    anchor_question = Column(Boolean, default=False)
    ccf_code = Column(String(1), nullable=False)
    question_code = Column(String(1))

    # relationships
    version = relationship("Version", back_populates="answer_key")
    responses = relationship("CandidateResponse", back_populates="answer_key")
    cwas = relationship("CommonWrongAnswer", back_populates="answer")

    # validation
    @validates('version_id', 'question_number')
    def generate_id(self, key, value):
        version_id = value if key == 'version_id' else self.version_id
        question_number = value if key == 'question_number' else self.question_number
        if version_id and question_number:
            self.answer_id = f"{version_id}_{question_number}"
        return value

    @validates('productive_answer', 'anchor_question')
    def convert_to_boolean(self, key, value):
        if isinstance(value, str):
            return value.strip().lower() in ('true', '1', 'yes', 'y')
        return bool(value)
    
    ## ADD IN SOME SORT OF AUTO FUNCTION TO GET CCF CODE


class CommonWrongAnswer(Base):
    """Table for automatically logging incorrect CandidateResponses to productive questions"""
    __tablename__ = "common_wrong_answers"

    # generated fields
    cwa_id = Column(Integer, primary_key=True, autoincrement=True)
    # provided fields
    version_id = Column(String, ForeignKey("versions.version_id"), nullable=False)
    answer_id = Column(String, ForeignKey("answer_keys.answer_id"), nullable=False)
    wrong_answer = Column(String, nullable=False)

    # relationships
    version = relationship("Version", back_populates="cwas")
    answer = relationship("AnswerKey", back_populates="cwas")


class Upload(Base):
    """Main table for this app. Each Upload represents a register uploaded by a centre, containing Batches and Candidates."""
    __tablename__ = 'uploads'

    # generated fields
    upload_id = Column(String, primary_key=True)
    # provided fields
    marking_window_id = Column(Integer, ForeignKey("marking_windows.marking_window_id"), nullable=False)
    centre_id = Column(String(4), ForeignKey("centres.centre_id"), nullable=False)
    part_delivery = Column(String(2), nullable=False)
    epd_number = Column(String(9))
    test_date = Column(Date)
    upload_date = Column(Date, server_default=func.now())
    rescan_needed = Column(Boolean, default=False)
    sent_date = Column(Date)

    # relationships
    marking_window = relationship("MarkingWindow", back_populates="uploads")
    centre = relationship("Centre", back_populates="uploads")
    batches = relationship("Batch", back_populates='upload', cascade="all, delete-orphan")
    candidates = relationship("Candidate", back_populates='upload', cascade="all, delete-orphan")

    # validation
    # @validates('marking_window_id', 'centre_id', 'part_delivery')
    # def generate_id(self, key, value):
    #     marking_window_id = value if key == 'marking_window_id' else self.marking_window_id
    #     centre_id = value if key == 'centre_id' else self.centre_id
    #     part_delivery = value if key == 'part_delivery' else self.part_delivery
        
    #     if marking_window_id and centre_id and part_delivery:
    #         self.upload_id = f"{marking_window_id}_{centre_id}_{part_delivery}"
    #     return value
    def __init__(self, marking_window_id=None, centre_id=None, part_delivery=None, 
                 epd_number=None, test_date=None, upload_date=None, 
                 rescan_needed=False, sent_date=None, **kwargs):
        # Set the required fields first
        self.marking_window_id = marking_window_id
        self.centre_id = centre_id
        self.part_delivery = part_delivery
        self.epd_number = epd_number
        self.test_date = test_date
        self.upload_date = upload_date
        self.rescan_needed = rescan_needed
        self.sent_date = sent_date
        
        # Generate the primary key
        if marking_window_id and centre_id and part_delivery:
            self.upload_id = f"{marking_window_id}_{centre_id}_{part_delivery}"
        
        # Call parent constructor with any remaining kwargs
        super().__init__(**kwargs)
    

class Batch(Base):
    """Helper table to link Upload, Candidates and FileUploads.
    One entry created per centre, per upload, per version*.
    Batches are assigned to examiners and markers.
    *Exception would be if Writing batch is over 50, then split it into a smaller batch."""
    __tablename__ = 'batches'

    # generated fields
    batch_id = Column(String, primary_key=True)
    # provided fields
    upload_id = Column(String, ForeignKey("uploads.upload_id"))
    version_id = Column(String, ForeignKey("versions.version_id"))
    component_id = Column(String, ForeignKey("components.component_id"))
    examiner_id = Column(Integer, ForeignKey('examiners.examiner_id')) # Writing Only

    # relationships
    upload = relationship("Upload", back_populates="batches")
    version = relationship("Version", back_populates="batches")
    component = relationship("Component", back_populates="batches")
    examiner = relationship('Examiner', back_populates='batches')
    writing_candidates = relationship("Candidate", back_populates="writing_batch", foreign_keys="Candidate.writing_batch_id", passive_deletes=True)
    reading_candidates = relationship("Candidate", back_populates="reading_batch", foreign_keys="Candidate.reading_batch_id", passive_deletes=True)
    listening_candidates = relationship("Candidate", back_populates="listening_batch", foreign_keys="Candidate.listening_batch_id", passive_deletes=True)  
    file_uploads = relationship("FileUpload", back_populates='batch')

    # validation
    # @validates('upload_id', 'version_id')
    # def generate_id(self, key, value):
    #     upload_id = value if key == 'upload_id' else self.upload_id
    #     version_id = value if key == 'version_id' else self.version_id
        
    #     if upload_id and version_id:
    #         self.batch_id = f"{upload_id}_{str(version_id)}"
    #     return value

    # @hybrid_property
    # def batch_id(self):
    #     return f"{self.upload_id}_{str(self.version_id)}"

    def __init__(self, upload_id=None, version_id=None, component_id=None, examiner_id=None, **kwargs):
        # Set the foreign key fields first
        self.upload_id = upload_id
        self.version_id = version_id
        self.component_id = component_id
        self.examiner_id = examiner_id
        
        # Generate the primary key
        if upload_id and version_id:
            self.batch_id = f"{upload_id}_{version_id}"
        
        # Call parent constructor with any remaining kwargs
        super().__init__(**kwargs)

# @event.listens_for(Batch, 'before_insert')
# def set_batch_id(mapper, connection, target):
#     if not target.batch_id and target.upload_id and target.version_id:
#         target.batch_id = f"{target.upload_id}_{target.version_id}"
    

class Candidate(Base):
    """Each entry represents one candidate. Candidate can belong to one Upload, and to one Batch for each component."""
    __tablename__ = 'candidates'

    # generated fields
    candidate_id = Column(String, primary_key=True)
    # inherited fields
    upload_id = Column(String, ForeignKey('uploads.upload_id'), nullable=False)
    # provided fields
    candidate_number = Column(Integer, nullable=False)
    candidate_name = Column(String, nullable=False)
    paper_sat = Column(String(2))
    writing_batch_id = Column(String, ForeignKey('batches.batch_id', ondelete="SET NULL"))
    reading_batch_id = Column(String, ForeignKey('batches.batch_id', ondelete="SET NULL"))
    listening_batch_id = Column(String, ForeignKey('batches.batch_id', ondelete="SET NULL"))
    writing_t1_ta = Column(Integer)
    writing_t1_cc = Column(Integer)
    writing_t1_lr = Column(Integer)
    writing_t1_gra = Column(Integer)
    writing_t2_ta = Column(Integer)
    writing_t2_cc = Column(Integer)
    writing_t2_lr = Column(Integer)
    writing_t2_gra = Column(Integer)
    writing_underlength = Column(Boolean)
    writing_off_topic = Column(Boolean)
    
    # CHECK CCF DATA FOR WHAT DATA WE NEED TO HAVE IN DATA STRINGS
    language_id = Column(Integer, ForeignKey('languages.language_id'))

    # relationships
    upload = relationship('Upload', back_populates='candidates')
    language = relationship("Language", back_populates="candidates")
    writing_batch = relationship("Batch", foreign_keys=[writing_batch_id], back_populates="writing_candidates")
    reading_batch = relationship("Batch", foreign_keys=[reading_batch_id], back_populates="reading_candidates")
    listening_batch = relationship("Batch", foreign_keys=[listening_batch_id], back_populates="listening_candidates")
    responses = relationship('CandidateResponse', back_populates='candidate')

    # validation
    # @validates("paper_sat")
    # def validate_paper(self, key, value):
    #     if value not in ("AC", "GT"):
    #         raise ValueError(f"Invalid paper value: {value}")
    #     return value
    
    # @validates('upload_id', 'candidate_number')
    # def generate_id(self, key, value):
    #     upload_id = value if key == 'upload_id' else self.upload_id
    #     candidate_number = value if key == 'candidate_number' else self.candidate_number
        
    #     if upload_id and candidate_number:
    #         self.candidate_id = f"{upload_id}_{str(candidate_number).zfill(4)}"
    #     return value
    def __init__(self, upload_id=None, candidate_number=None, candidate_name=None, 
                 paper_sat=None, writing_batch_id=None, reading_batch_id=None, 
                 listening_batch_id=None, writing_t1_ta=None, writing_t1_cc=None, 
                 writing_t1_lr=None, writing_t1_gra=None, writing_t2_ta=None, 
                 writing_t2_cc=None, writing_t2_lr=None, writing_t2_gra=None, 
                 writing_underlength=None, writing_off_topic=None, language_id=None, **kwargs):
        
        # Set the required fields first
        self.upload_id = upload_id
        self.candidate_number = candidate_number
        self.candidate_name = candidate_name
        
        # Validate paper_sat before setting
        if paper_sat is not None and paper_sat not in ("AC", "GT"):
            raise ValueError(f"Invalid paper value: {paper_sat}")
        self.paper_sat = paper_sat
        
        # Set optional fields
        self.writing_batch_id = writing_batch_id
        self.reading_batch_id = reading_batch_id
        self.listening_batch_id = listening_batch_id
        self.writing_t1_ta = writing_t1_ta
        self.writing_t1_cc = writing_t1_cc
        self.writing_t1_lr = writing_t1_lr
        self.writing_t1_gra = writing_t1_gra
        self.writing_t2_ta = writing_t2_ta
        self.writing_t2_cc = writing_t2_cc
        self.writing_t2_lr = writing_t2_lr
        self.writing_t2_gra = writing_t2_gra
        self.writing_underlength = writing_underlength
        self.writing_off_topic = writing_off_topic
        self.language_id = language_id
        
        # Generate the primary key
        if upload_id and candidate_number is not None:
            self.candidate_id = f"{upload_id}_{str(candidate_number).zfill(4)}"
        
        # Call parent constructor with any remaining kwargs
        super().__init__(**kwargs)

    @validates("paper_sat")
    def validate_paper(self, key, value):
        if value is not None and value not in ("AC", "GT"):
            raise ValueError(f"Invalid paper value: {value}")
        return value


class CandidateResponse(Base):
    """Each entry represents a candidates' response to one Reading & Listening question. Can be compared to AnswerKey table for automarking."""
    __tablename__ = 'candidate_responses'

    # generated fields
    response_id = Column(Integer, primary_key=True, autoincrement=True)
    answer_id = Column(String, ForeignKey('answer_keys.answer_id'), nullable=True)
    # provided fields
    candidate_id = Column(String, ForeignKey('candidates.candidate_id'))
    version_id = Column(String, ForeignKey('versions.version_id'), nullable=False)
    question_number = Column(Integer, nullable=False)
    response = Column(String)

    # relationships
    candidate = relationship('Candidate', back_populates='responses')
    version = relationship('Version', back_populates='responses')
    answer_key = relationship('AnswerKey', back_populates='responses')

    # validation
    @validates('version_id', 'question_number')
    def generate_id(self, key, value):
        version_id = value if key == 'version_id' else self.version_id
        question_number = value if key == 'question_number' else self.question_number
        
        if version_id and question_number:
            self.answer_id = f"{version_id}_{question_number}"
        return value


class FileUpload(Base):
    """Each entry represents one file, uploaded to FTP server. Files are linked to specific Batches, specific versions, and part of a specific Upload"""
    __tablename__ = 'file_uploads'

    # generated fields
    file_upload_id = Column(Integer, primary_key=True, autoincrement=True)
    # inherited fields
    batch_id = Column(String, ForeignKey('batches.batch_id'), nullable=False)
    # provided fields
    file_name = Column(String, nullable=False)
    is_rescan = Column(Boolean, default=False)

    # relationships
    batch = relationship('Batch', back_populates='file_uploads')


class StagedFile(Base):
    __tablename__ = 'staged_files'
    
    # generated fields
    file_id = Column(Integer, primary_key=True, autoincrement=True)
    upload_date = Column(Date, server_default=func.now())
    # inputted fields
    centre_id = Column(String, nullable=False)
    marking_window_id = Column(Integer, nullable=False)
    version_id = Column(String, nullable=False)
    destination_filename = Column(String, nullable=False)
    destination_folder = Column(String, nullable=False)
    temp_path = Column(String, nullable=False)


def get_model_by_tablename(tablename: str):
    """Uses table name to return the relevant ORM model class"""
    for mapper in Base.registry.mappers:
        model = mapper.class_
        if hasattr(model, "__tablename__") and model.__tablename__ == tablename:
            return model
    return None