from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Column, Field, Relationship, SQLModel


class RDSModel(SQLModel):
    model_config = {"json_schema_extra": {"exclude": True}}


class Corpus(RDSModel, table=True):
    __tablename__ = "corpus"
    import_id: str | None = Field(default=None, primary_key=True)
    title: str
    corpus_type_name: str
    corpus_text: str
    corpus_image_url: str


class FamilyCorpusLink(RDSModel, table=True):
    __tablename__ = "family_corpus"
    corpus_import_id: int | None = Field(
        default=None, foreign_key="corpus.import_id", primary_key=True
    )
    family_import_id: int | None = Field(
        default=None, foreign_key="family.import_id", primary_key=True
    )


class FamilyGeographyLink(RDSModel, table=True):
    __tablename__ = "family_geography"
    geography_id: int | None = Field(
        default=None, foreign_key="geography.id", primary_key=True
    )
    family_import_id: int | None = Field(
        default=None, foreign_key="family.import_id", primary_key=True
    )


class GeographyBase(RDSModel):
    id: int | None = Field(default=None, primary_key=True)
    display_value: str
    value: str
    type: str
    slug: str


class Geography(GeographyBase, table=True):
    __tablename__ = "geography"
    parent_id: int = Field(foreign_key="geography.id")
    # the relationship stuff here is a little non-standard
    # there doesn't seem to be an easier way to do this with RDSModel
    parent: Optional["Geography"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "[Geography.id]"},
    )
    children: list["Geography"] = Relationship(back_populates="parent")
    families: list["Family"] = Relationship(
        back_populates="geographies", link_model=FamilyGeographyLink
    )


class GeographyPublic(GeographyBase):
    parent: Optional["Geography"]
    children: list["Geography"]


# Family
class FamilyCategory(str, Enum):
    EXECUTIVE = "Executive"
    LEGISLATIVE = "Legislative"
    UNFCCC = "UNFCCC"
    MCF = "MCF"
    REPORTS = "Reports"


class FamilyMetadataBase(RDSModel):
    pass


class FamilyMetadata(FamilyMetadataBase, table=True):
    __tablename__ = "family_metadata"
    family_import_id: str | None = Field(
        default=None, foreign_key="family.import_id", primary_key=True
    )
    value: Dict = Field(sa_column=Column(JSONB))
    family: "Family" = Relationship(back_populates="family_metadata")


class FamilyMetadataPublic(FamilyMetadataBase):
    value: Dict[str, Any]


class FamilyBase(RDSModel):
    import_id: str | None = Field(default=None, primary_key=True)
    description: str | None
    family_category: FamilyCategory
    created: datetime
    # TODO: Not sure why last_modified is not working
    # last_modifed: datetime


class Family(FamilyBase, table=True):
    __tablename__ = "family"
    geographies: list[Geography] = Relationship(
        back_populates="families", link_model=FamilyGeographyLink
    )
    family_documents: list["FamilyDocument"] = Relationship(back_populates="family")
    family_metadata: FamilyMetadata = Relationship(back_populates="family")
    slug: Optional["Slug"] = Relationship(back_populates="family")


class FamilyPublic(FamilyBase):
    model_config = {"json_schema_extra": {"exclude": True}}
    geographies: list[GeographyPublic]
    family_metadata: FamilyMetadataPublic


# This is to avoid self-referentiality in FamilyDocument
# But allow us to show the doc on the /families endpoint
class FamilyPublicWithFamilyDocuments(FamilyBase):
    geographies: list[GeographyPublic] | None
    family_documents: list["FamilyDocument"] | None


class DocumentStatus(str, Enum):
    CREATED = "Created"
    PUBLISHED = "Published"
    DELETED = "Deleted"


class Slug(RDSModel, table=True):
    __tablename__ = "slug"
    name: int | None = Field(default=None, primary_key=True)
    family_document: Optional["FamilyDocument"] = Relationship(back_populates="slug")
    family: Optional["Family"] = Relationship(back_populates="slug")
    family_import_id: str | None = Field(default=None, foreign_key="family.import_id")
    family_document_import_id: str | None = Field(
        default=None, foreign_key="family_document.import_id"
    )


# FamilyDocument
class FamilyDocumentBase(RDSModel):
    import_id: str | None = Field(default=None, primary_key=True)
    variant_name: str | None
    document_status: DocumentStatus | None
    created: datetime
    # TODO: Not sure why last_modified is not working
    # last_modifed: datetime


class FamilyDocument(FamilyDocumentBase, table=True):
    __tablename__ = "family_document"
    family_import_id: str | None = Field(default=None, foreign_key="family.import_id")
    family: Family = Relationship(back_populates="family_documents")
    physical_document_id: int = Field(foreign_key="physical_document.id", unique=True)
    physical_document: Optional["PhysicalDocument"] = Relationship(
        back_populates="family_document"
    )
    valid_metadata: Dict = Field(sa_column=Column(JSONB))
    slug: Optional[Slug] = Relationship(back_populates="family_document")


class FamilyDocumentPublic(FamilyDocumentBase):
    # @computed_field
    # def metadata(self) -> list[dict[str, Any]]:
    #     authors = self.family.family_metadata.value["author"]
    #     author_types = self.family.family_metadata.value["author_type"]
    #     filtered_metadata = {
    #         k: v
    #         for k, v in self.family.family_metadata.value.items()
    #         if k not in ["author", "author_type"]
    #     }
    #     return {
    #         **filtered_metadata,
    #         "authors": [
    #             {"name": name, "type": type_}
    #             for name, type_ in zip(authors, author_types)
    #         ],
    #     }

    family: FamilyPublic
    physical_document: Optional["PhysicalDocument"]


# PhysicalDocument
class PhysicalDocumentBase(RDSModel):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    md5_sum: str
    source_url: str
    content_type: str
    cdn_object: str


class PhysicalDocument(PhysicalDocumentBase, table=True):
    __tablename__ = "physical_document"
    family_document: Optional[FamilyDocument] = Relationship(
        back_populates="physical_document"
    )
