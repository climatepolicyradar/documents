from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class DocumentStatus(str, Enum):
    CREATED = "Created"
    PUBLISHED = "Published"
    DELETED = "Deleted"


class Variant(str, Enum):
    ORIGINAL_LANGUAGE = "Original Language"
    TRANSLATION = "Translation"


class Role(str, Enum):
    DOCUMENT_STORED_ON_WEBPAGE = "DOCUMENT(S) STORED ON WEBPAGE"
    PREVIOUS_VERSION = "PREVIOUS VERSION"
    INFORMATION_WEBPAGE = "INFORMATION WEBPAGE"
    SUPPORTING_DOCUMENTATION = "SUPPORTING DOCUMENTATION"
    SUPPORTING_LEGISLATION = "SUPPORTING LEGISLATION"
    SUMMARY = "SUMMARY"
    PRESS_RELEASE = "PRESS RELEASE"
    ANNEX = "ANNEX"
    AMENDMENT = "AMENDMENT"
    MAIN = "MAIN"


class Type(str, Enum):
    CRITERIA = "Criteria"
    NATIONAL_ADAPTATION_PLAN_ADAPTATION_COMMUNICATION = (
        "National Adaptation Plan,Adaptation Communication"
    )
    PRE_SESSION_DOCUMENT_PROGRESS_REPORT = "Pre-Session Document,Progress Report"
    NATIONAL_COMMUNICATION = "National Communication"
    ROADMAP = "Roadmap"
    DISCUSSION_PAPER = "Discussion Paper"
    EU_DECISION = "EU Decision"
    PRE_SESSION_DOCUMENT_SYNTHESIS_REPORT = "Pre-Session Document,Synthesis Report"
    PRE_SESSION_DOCUMENT = "Pre-Session Document"
    NATIONALLY_DETERMINED_CONTRIBUTION = "Nationally Determined Contribution"
    BILL = "Bill"
    BIENNIAL_REPORT = "Biennial Report"
    ADAPTATION_COMMUNICATION = "Adaptation Communication"
    LAW = "Law"
    DECISION_AND_PLAN = "Decision and Plan"
    EXECUTIVE_ORDER = "Executive Order"
    CORPORATE_REGULATORY_FILING = "Corporate regulatory filing"
    REPORT = "Report"
    PROJECT_COMPLETION_REPORT = "Project completion report"
    ASSESSMENT = "Assessment"
    ORDINANCE = "Ordinance"
    EU_DIRECTIVE = "EU Directive"
    STRATEGIC_ASSESSMENT = "Strategic Assessment"
    SUBMISSION_TO_THE_GLOBAL_STOCKTAKE = "Submission to the Global Stocktake"
    GLOBAL_STOCKTAKE_SYNTHESIS_REPORT = "Global Stocktake Synthesis Report"
    ACTION_PLAN = "Action Plan"
    CONSTITUTION = "Constitution"
    VISION = "Vision"
    ACCORD = "Accord"
    NATIONALLY_DETERMINED_CONTRIBUTION_ADAPTATION_COMMUNICATION = (
        "Nationally Determined Contribution,Adaptation Communication"
    )
    APPROVED_FUNDING_PROPOSAL = "Approved funding proposal"
    REGULATION = "Regulation"
    ACT = "Act"
    RESOLUTION = "Resolution"
    OTHER = "Other"
    EDICT = "Edict"
    TECHNICAL_ANALYSIS_SUMMARY_REPORT = "Technical Analysis Summary Report"
    ROYAL_DECREE = "Royal Decree"
    ANNEX = "Annex"
    IPCC_REPORT = "IPCC Report"
    TECHNICAL_ANALYSIS_TECHNICAL_REPORT = "Technical Analysis Technical Report"
    SUMMARY_REPORT = "Summary Report"
    FACILITATIVE_SHARING_OF_VIEWS_REPORT = "Facilitative Sharing of Views Report"
    PUBLICATION = "Publication"
    BIENNIAL_UPDATE_REPORT = "Biennial Update Report"
    CORPORATE_VOLUNTARY_REPORT = "Corporate voluntary report"
    LAW_AND_PLAN = "Law and Plan"
    NATIONAL_COMMUNICATION_BIENNIAL_UPDATE_REPORT = (
        "National Communication,Biennial Update Report"
    )
    STATEMENT = "Statement"
    ORDER = "Order"
    SUMMARY = "Summary"
    NATIONALLY_DETERMINED_CONTRIBUTION_NATIONAL_COMMUNICATION = (
        "Nationally Determined Contribution,National Communication"
    )
    PROTOCOL = "Protocol"
    DECISION = "Decision"
    INTERSESSIONAL_DOCUMENT = "Intersessional Document"
    NATIONAL_INVENTORY_REPORT = "National Inventory Report"
    FRAMEWORK = "Framework"
    POLICY = "Policy"
    PLAN = "Plan"
    PRESS_RELEASE = "Press Release"
    RULES = "Rules"
    STRATEGY = "Strategy"
    NATIONAL_ADAPTATION_PLAN = "National Adaptation Plan"
    PROGRAMME = "Programme"
    PROGRESS_REPORT = "Progress Report"
    BIENNIAL_REPORT_NATIONAL_COMMUNICATION = "Biennial Report,National Communication"
    FAST_START_FINANCE_REPORT = "Fast-Start Finance Report"
    NATIONAL_COMMUNICATION_BIENNIAL_REPORT = "National Communication,Biennial Report"
    LONG_TERM_LOW_EMISSION_DEVELOPMENT_STRATEGY = (
        "Long-Term Low-Emission Development Strategy"
    )
    PUBLICATION_REPORT = "Publication,Report"
    DIRECTIVE = "Directive"
    AGENDA = "Agenda"
    DECREE_LAW = "Decree Law"
    SYNTHESIS_REPORT = "Synthesis Report"
    BIENNIAL_UPDATE_REPORT_NATIONAL_COMMUNICATION = (
        "Biennial Update Report,National Communication"
    )
    EU_REGULATION = "EU Regulation"
    DECREE = "Decree"
    PRE_SESSION_DOCUMENT_ANNUAL_COMPILATION_AND_ACCOUNTING_REPORT = (
        "Pre-Session Document,Annual Compilation and Accounting Report"
    )
    GUIDANCE = "Guidance"


class Category(str, Enum):
    EXECUTIVE = "Executive"
    LEGISLATIVE = "Legislative"
    UNFCCC = "UNFCCC"
    MCF = "MCF"
    REPORTS = "Reports"


class Geography(SQLModel):
    id: int | None
    display_value: str
    value: str
    type: str
    slug: str


class EventStatus(str, Enum):
    REPEALED_REPLACED = "Repealed/Replaced"
    ENTERED_INTO_FORCE = "Entered Into Force"
    PASSED_APPROVED = "Passed/Approved"
    FILING = "Filing"
    UPDATED = "Updated"
    PUBLISHED = "Published"
    PROJECT_APPROVED = "Project Approved"
    CONCEPT_APPROVED = "Concept Approved"
    NET_ZERO_PLEDGE = "Net Zero Pledge"
    OTHER = "Other"
    SETTLED = "Settled"
    IMPLEMENTATION_DETAILS = "Implementation Details"
    CLOSED = "Closed"
    PROJECT_COMPLETED = "Project Completed"
    UNDER_IMPLEMENTATION = "Under Implementation"
    SET = "Set"
    CANCELLED = "Cancelled"
    AMENDED = "Amended"


class EventType(str, Enum):
    REPEALED_REPLACED = "Repealed/Replaced"
    ENTERED_INTO_FORCE = "Entered Into Force"
    PASSED_APPROVED = "Passed/Approved"
    FILING = "Filing"
    UPDATED = "Updated"
    PUBLISHED = "Published"
    PROJECT_APPROVED = "Project Approved"
    CONCEPT_APPROVED = "Concept Approved"
    NET_ZERO_PLEDGE = "Net Zero Pledge"
    OTHER = "Other"
    SETTLED = "Settled"
    IMPLEMENTATION_DETAILS = "Implementation Details"
    CLOSED = "Closed"
    PROJECT_COMPLETED = "Project Completed"
    UNDER_IMPLEMENTATION = "Under Implementation"
    SET = "Set"
    CANCELLED = "Cancelled"
    AMENDED = "Amended"


class Event(SQLModel):
    title: str
    date: datetime
    type: EventType
    status: EventStatus


class CorpusType(str, Enum):
    GCF = "GCF"
    GEF = "GEF"
    AF = "AF"
    LAWS_AND_POLICIES = "Laws and Policies"
    CIF = "CIF"
    INTL_AGREEMENTS = "Intl. agreements"
    REPORTS = "Reports"


class Corpus(SQLModel):
    id: str
    title: str
    description: str
    image: str
    type: CorpusType


class Family(SQLModel):
    id: str
    title: str
    description: str


class Collection(SQLModel):
    id: str
    title: str
    description: str


class DocumentBase(SQLModel):
    # ids
    id: str
    slug: str


class LabelType(str, Enum):
    GEOGRAPHY = "Geography"


class Label(SQLModel):
    id: str
    label: str
    type: LabelType


class DocumentPublic(DocumentBase):
    # ids
    id: str
    slug: str
    labels: list[Label] = []

    # family
    description: str
    category: Category
    geography: Geography
    # metadata: list[str]

    # family_document
    # role: Role
    # type: Type
    variant: Variant
    status: DocumentStatus
    # valid_metadata
    role: Role
    type: Type

    # physical_document
    title: str
    md5_sum: str
    source_url: str
    content_type: str
    cdn_object: str
    # relationships
    language: str

    # relationships
    corpuses: list[Corpus] = []
    families: list[Family] = []
    collections: list[Collection] = []
    events: list[Event] = []

    # family_metadata
    metadata_instrument: list[str] = []
    metadata_implementing_agency: list[str] = []
    metadata_topic: list[str] = []
    metadata_framework: list[str] = []
    metadata_theme: list[str] = []
    metadata_event_type: list[str] = []
    metadata_project_url: list[str] = []
    metadata_status: list[str] = []
    metadata_approved_ref: list[str] = []
    metadata_focal_area: list[str] = []
    metadata_project_value_fund_spend: list[str] = []
    metadata_hazard: list[str] = []
    metadata_author: list[str] = []
    metadata_sector: list[str] = []
    metadata_author_type: list[str] = []
    metadata_project_value_co_financing: list[str] = []
    metadata_result_type: list[str] = []
    metadata_result_area: list[str] = []
    metadata_keyword: list[str] = []
    metadata_project_id: list[str] = []
    metadata_external_id: list[str] = []
    metadata_region: list[str] = []


class Document(DocumentBase, table=True):
    __tablename__ = "documents"
    id: str | None = Field(default=None, primary_key=True)
    title: str
