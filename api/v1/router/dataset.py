from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError

from core import Session, db, logger, verify_user
from schema import Dataset, Metadata, Page, Tag

router = APIRouter()


@router.post("/", response_model=Dataset)
async def create_dataset(
    input: Dataset,
    session: Session = Depends(db.get_session),
    user=Depends(verify_user),
):
    """
    Use this endpoint to create a new dataset
    """
    try:
        dataset = Dataset(**input.model_dump(exclude=Dataset.get_ignored_fields()))
        active_datasets_count = (
            session.query(Metadata)
            .filter(Metadata.item == "active_datasets_count")
            .first()
        )

        if active_datasets_count is None:
            active_datasets_count = Metadata(item="active_datasets_count", value=0)
            session.add(active_datasets_count)

        active_datasets_count.value += 1

        session.add(dataset)
        session.commit()
        return dataset.to_dict()
    except IntegrityError as e:
        session.rollback()
        logger.error(e._message())
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=e._message())
    except Exception as e:
        session.rollback()
        logger.error(str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/", response_model=Page[Dataset])
async def get_datasets(
    page: int = 1,
    limit: int = Query(10, ge=1, le=100, description="Number of datasets to return"),
    session: Session = Depends(db.get_session),
):
    """
    Use this endpoint to get lists of datasets
    """

    try:
        datasets = (
            session.query(Dataset)
            .filter(Dataset.deleted_at == None)
            .limit(limit)
            .offset((page - 1) * limit)
            .all()
        )
        return Page[Dataset](
            items=datasets,
            page=page,
            limit=limit,
            item_count=int(
                session.query(Metadata)
                .filter(Metadata.item == "active_datasets_count")
                .first()
                .value
            ),
        )
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/search", response_model=Page[Dataset])
async def search_datasets(
    page: int = 1,
    limit: int = Query(10, ge=1, le=100, description="Number of datasets to return"),
    name: str = None,
    source: str = None,
    license: str = None,
    tags: List[str] = None,
    session: Session = Depends(db.get_session),
):
    """
    Use this endpoint to search datasets
    """

    try:
        datasets = session.query(Dataset).filter(Dataset.deleted_at == None)
        if name:
            datasets = datasets.filter(Dataset.name.ilike(f"%{name}%"))
        if source:
            datasets = datasets.filter(Dataset.source.ilike(f"%{source}%"))
        if license:
            datasets = datasets.filter(Dataset.license.ilike(f"%{license}%"))
        if tags:
            datasets = datasets.filter(Dataset.tags.any(Tag.name.in_(tags)))

        datasets = datasets.limit(limit).offset((page - 1) * limit).all()
        return Page[Dataset](
            items=[dataset.to_dict() for dataset in datasets],
            page=page,
            limit=limit,
            item_count=len(datasets),
        )
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{dataset_id}", response_model=Dataset)
async def get_dataset(dataset_id: str, session: Session = Depends(db.get_session)):
    """
    Use this endpoint to get a specific dataset
    """

    try:
        dataset = (
            session.query(Dataset)
            .filter(Dataset.id == dataset_id, Dataset.deleted_at == None)
            .first()
        )
        return dataset
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/tags/{dataset_id}", response_model=List[Tag])
async def get_tags_for_dataset(
    dataset_id: str, session: Session = Depends(db.get_session)
):
    """
    Use this endpoint to get all tags for a specific dataset
    """

    try:
        dataset = (
            session.query(Dataset)
            .filter(Dataset.id == dataset_id, Dataset.deleted_at == None)
            .first()
        )
        return [tag for tag in dataset.tags if tag.deleted_at == None]
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/add_tag/{dataset_id}/{tag_id}", response_model=Dataset)
async def add_tag_to_dataset(
    dataset_id: str, tag_id: str, session: Session = Depends(db.get_session)
):
    """
    Use this endpoint to add a tag to a specific dataset
    """
    try:
        dataset = (
            session.query(Dataset)
            .filter(Dataset.id == dataset_id, Dataset.deleted_at == None)
            .first()
        )
        if dataset is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Dataset not found")

        tag = (
            session.query(Tag).filter(Tag.id == tag_id, Tag.deleted_at == None).first()
        )
        if tag is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tag not found")

        if tag in dataset.tags:
            return dataset

        dataset.tags.append(tag)
        session.commit()
        return dataset
    except Exception as e:
        session.rollback()
        logger.error(str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.patch("/remove_tag/{dataset_id}/{tag_id}", response_model=Dataset)
async def remove_tag_from_dataset(
    dataset_id: str, tag_id: str, session: Session = Depends(db.get_session)
):
    """
    Use this endpoint to remove a tag from a specific dataset
    """

    try:
        dataset = (
            session.query(Dataset)
            .filter(Dataset.id == dataset_id, Dataset.deleted_at == None)
            .first()
        )
        if not dataset:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Dataset not found")

        tag = (
            session.query(Tag).filter(Tag.id == tag_id, Tag.deleted_at == None).first()
        )
        if not tag:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Tag not found")

        dataset.tags.remove(tag)
        session.commit()
        return dataset
    except Exception as e:
        session.rollback()
        logger.error(str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


# @router.put("/upvote/{dataset_id}")
# async def upvote_dataset(dataset_id: str, session: Session = Depends(db.get_session)):
#     """
#     Use this endpoint to upvote a specific dataset
#     """

#     dataset = session.query(Dataset).filter(Dataset.id == dataset_id, Dataset.deleted_at == None).first()
#     if not dataset:
#         raise HTTPException(status.HTTP_404_NOT_FOUND)

#     dataset.votes += 1
#     session.commit()
#     return dataset.to_dict()


@router.patch("/{dataset_id}", response_model=Dataset)
async def update_dataset(
    dataset_id: str, input: Dataset, session: Session = Depends(db.get_session)
):
    """
    Use this endpoint to update a specific dataset
    """

    try:
        dataset = (
            session.query(Dataset)
            .filter(Dataset.id == dataset_id, Dataset.deleted_at == None)
            .first()
        )
        if not dataset:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Dataset not found")

        dataset.update(
            **input.model_dump(exclude=Dataset.get_ignored_fields(), exclude_unset=True)
        )
        session.commit()
        return dataset
    except IntegrityError as e:
        session.rollback()
        logger.error(e._message())
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=e._message())
    except Exception as e:
        session.rollback()
        logger.error(str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{dataset_id}", response_model=str)
async def delete_dataset(dataset_id: str, session: Session = Depends(db.get_session)):
    """
    Use this endpoint to delete a specific dataset
    """

    try:
        dataset = (
            session.query(Dataset)
            .filter(Dataset.id == dataset_id, Dataset.deleted_at == None)
            .first()
        )
        if not dataset:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        if dataset.deleted_at:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        dataset.update(
            deleted_at=datetime.now(timezone.utc), name=f"deleted_{dataset.name}"
        )
        active_datasets_count = (
            session.query(Metadata)
            .filter(Metadata.item == "active_datasets_count")
            .first()
        )
        active_datasets_count.value -= 1
        session.commit()
        return dataset.id
    except Exception as e:
        session.rollback()
        logger.error(str(e))
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
