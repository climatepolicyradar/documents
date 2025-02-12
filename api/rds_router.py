from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from rds_models import (
    Family,
    FamilyDocument,
    FamilyDocumentPublic,
    FamilyMetadata,
    FamilyPublicWithFamilyDocuments,
)

# from rds import FamilyDocument
from sqlmodel import Session, create_engine, select

router = APIRouter(prefix="/rds", tags=["rds"], include_in_schema=False)


navigator_engine = create_engine(
    # This just matches the docker-compose.yml file
    str("postgresql://navigator:navigator@localhost/navigator")
)


def get_navigator_session():
    with Session(navigator_engine) as session:
        yield session


NavigatorSessionDep = Annotated[Session, Depends(get_navigator_session)]


@router.get("/")
def read_root():
    return {"service": "documents/rds"}


@router.get("/family_documents")
def read_family_documents(
    session: NavigatorSessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[FamilyDocumentPublic]:
    family_documents = session.exec(
        select(FamilyDocument).offset(offset).limit(limit)
    ).all()

    if not family_documents:
        raise HTTPException(status_code=404, detail="Documents not found")

    return family_documents


@router.get("/family_documents/{document_id}")
def read_family_document(
    document_id: str, session: NavigatorSessionDep
) -> FamilyDocumentPublic:
    family_document = session.get(FamilyDocument, document_id)

    if not family_document:
        raise HTTPException(status_code=404, detail="Document not found")

    return family_document


@router.get("/family_documents_metadata")
def read_family_documents_metadata(
    session: NavigatorSessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=15000)] = 15000,
):
    family_documents = session.exec(
        select(FamilyDocument).offset(offset).limit(limit)
    ).all()

    if not family_documents:
        raise HTTPException(status_code=404, detail="Documents not found")

    keys = set()
    for family_document in family_documents:
        if set(family_document.valid_metadata.keys()) != {"role", "type"}:
            print(family_document.valid_metadata)

        keys.update(family_document.valid_metadata.keys())

    return keys


@router.get("/families")
def read_families(
    session: NavigatorSessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    families = session.exec(select(Family).offset(offset).limit(limit)).all()

    if not families:
        raise HTTPException(status_code=404, detail="Families not found")

    return families


@router.get("/families/{family_id}")
def read_family(
    family_id: str, session: NavigatorSessionDep
) -> FamilyPublicWithFamilyDocuments:
    family = session.get(Family, family_id)

    if not family:
        raise HTTPException(status_code=404, detail="Family not found")

    return family


@router.get("/family_metadata")
def read_family_metadata(
    session: NavigatorSessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=10000)] = 10000,
):
    family_metadata = session.exec(
        select(FamilyMetadata).offset(offset).limit(limit)
    ).all()

    if not family_metadata:
        raise HTTPException(status_code=404, detail="Family not found")

    keys = set()
    for metadata in family_metadata:
        keys.update(metadata.value.keys())

    keys_with_amounts = {}
    for key in keys:
        for metadata in family_metadata:
            if key in metadata.value:
                if keys_with_amounts.get(key):
                    keys_with_amounts[key] += 1
                else:
                    keys_with_amounts[key] = 1

    return keys_with_amounts


class DocumentFields(FamilyPublicWithFamilyDocuments):
    # family
    project_value_fund_spend: list[str]
    project_id: list[str]
    region: list[str]
    project_url: list[str]
    hazard: list[str]
    approved_ref: list[str]
    theme: list[str]
    framework: list[str]
    external_id: list[str]
    topic: list[str]
    author: list[str]
    result_area: list[str]
    status: list[str]
    project_value_co_financing: list[str]
    event_type: list[str]
    keyword: list[str]
    implementing_agency: list[str]
    instrument: list[str]
    result_type: list[str]
    focal_area: list[str]
    author_type: list[str]
    sector: list[str]
    # _document
    role: list[str]
    type: list[str]
