from typing import Annotated

from documents_model import (
    Category,
    Document,
    DocumentPublic,
    DocumentStatus,
    Geography,
    LabelType,
    Role,
    Type,
    Variant,
)
from fastapi import APIRouter, Depends, HTTPException, Query
from rds_models import FamilyDocument
from rds_router import NavigatorSessionDep
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel, select

router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)


documents_engine = create_engine(
    # This just matches the docker-compose.yml file
    str("postgresql://documents:documents@localhost:5433/documents")
)


def get_documents_session():
    with Session(documents_engine) as session:
        yield session


DocumentsSessionDep = Annotated[Session, Depends(get_documents_session)]


@router.get("/", response_model=list[DocumentPublic])
def get_documents(
    navigator_session: NavigatorSessionDep,
    documents_session: DocumentsSessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    write: bool = False,
):

    # Read from RDS
    family_documents = navigator_session.exec(
        select(FamilyDocument).offset(offset).limit(limit)
    ).all()

    if not family_documents:
        raise HTTPException(status_code=404, detail="Documents not found")

    # Transform to Document
    documents_public = [
        DocumentPublic(
            # ids
            id=family_document.import_id,
            slug=family_document.slug.name,
            labels=[
                {
                    "id": geography.value,
                    "type": LabelType.GEOGRAPHY,
                    "label": geography.display_value,
                }
                for geography in family_document.family.geographies
            ],
            # family
            description="",
            category=Category.LEGISLATIVE,
            geography=Geography(id=None, display_value="", value="", type="", slug=""),
            # metadata: list[str]
            # family_document
            variant=Variant.ORIGINAL_LANGUAGE,
            status=DocumentStatus.PUBLISHED,
            # valid_metadata
            role=Role.PRESS_RELEASE,
            type=Type.CRITERIA,
            # physical_document
            title=family_document.physical_document.title,
            md5_sum="",
            source_url="",
            content_type="",
            cdn_object="",
            # relationships
            language="",
            # relationships
            corpuses=[],
            families=[],
            collections=[],
            events=[],
            # family_metadata
            metadata_instrument=[],
            metadata_implementing_agency=[],
            metadata_topic=[],
            metadata_framework=[],
            metadata_theme=[],
            metadata_event_type=[],
            metadata_project_url=[],
            metadata_status=[],
            metadata_approved_ref=[],
            metadata_focal_area=[],
            metadata_project_value_fund_spend=[],
            metadata_hazard=[],
            metadata_author=[],
            metadata_sector=[],
            metadata_author_type=[],
            metadata_project_value_co_financing=[],
            metadata_result_type=[],
            metadata_result_area=[],
            metadata_keyword=[],
            metadata_project_id=[],
            metadata_external_id=[],
            metadata_region=[],
        )
        for family_document in family_documents
    ]

    # Transform to the DB Model
    # Write if we have ?write=true in the URL for funsies
    if write:
        documents_db = [
            Document(
                id=family_document.import_id,
                slug="slug",
                title=family_document.physical_document.title,
                labels=[],
            )
            for family_document in family_documents
        ]

        for document in documents_db:
            documents_session.merge(document)
        documents_session.commit()

    # Return the public model
    return documents_public


SQLModel.metadata.tables["documents"].create(documents_engine, checkfirst=True)
