from fastapi import APIRouter, Depends, HTTPException
from core import db, Session
from schema import Dataset, Tag
from datetime import datetime, timezone
from typing import List


router = APIRouter()


@router.post("/")
async def create_dataset(input: Dataset, session: Session = Depends(db.get_session)):
    """
    Use this endpoint to create a new dataset
    """
    dataset = Dataset(**input.model_dump(exclude=Dataset.get_ignored_fields()))

    try:
        session.add(dataset)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(400)
    return dataset.to_dict()


@router.get("/")
async def get_all_datasets(session: Session = Depends(db.get_session)):
    """
    Use this endpoint to get all datasets
    """

    datasets = session.query(Dataset).filter(Dataset.deleted_at == None).all()
    return [dataset.to_dict() for dataset in datasets]


@router.get("/search")
async def search_datasets(name: str = None, source: str = None, license: str = None, tags: List[str] = None, session: Session = Depends(db.get_session)):
    """
    Use this endpoint to search datasets
    """

    datasets = session.query(Dataset).filter(Dataset.deleted_at == None)
    if name:
        datasets = datasets.filter(Dataset.name.ilike(f"%{name}%"))
    if source:
        datasets = datasets.filter(Dataset.source.ilike(f"%{source}%"))
    if license:
        datasets = datasets.filter(Dataset.license.ilike(f"%{license}%"))
    if tags:
        datasets = datasets.filter(Dataset.tags.any(Tag.name.in_(tags)))
    return [dataset.to_dict() for dataset in datasets.all()]


@router.get("/{dataset_id}")
async def get_dataset(dataset_id: str, session: Session = Depends(db.get_session)):
    """
    Use this endpoint to get a specific dataset
    """

    dataset = session.query(Dataset).filter(Dataset.id == dataset_id, Dataset.deleted_at == None).first()
    if not dataset:
        raise HTTPException(404)
    return dataset.to_dict()


@router.get("/tags/{dataset_id}")
async def get_tags_for_dataset(dataset_id: str, session: Session = Depends(db.get_session)):
    """
    Use this endpoint to get all tags for a specific dataset
    """

    dataset = session.query(Dataset).filter(Dataset.id == dataset_id, Dataset.deleted_at == None).first()
    if not dataset:
        raise HTTPException(404)
    return [tag.to_dict() for tag in dataset.tags if tag.deleted_at == None]


@router.put("/add_tag/{dataset_id}/{tag_id}")
async def add_tag_to_dataset(dataset_id: str, tag_id: str, session: Session = Depends(db.get_session)):
    """
    Use this endpoint to add a tag to a specific dataset
    """

    dataset = session.query(Dataset).filter(Dataset.id == dataset_id, Dataset.deleted_at == None).first()
    if not dataset:
        print("here")
        raise HTTPException(404)

    tag = session.query(Tag).filter(Tag.id == tag_id, Tag.deleted_at == None).first()
    if not tag:
        print('there')
        raise HTTPException(404)

    dataset.tags.append(tag)
    session.commit()
    return dataset.to_dict()


@router.put("/remove_tag/{dataset_id}/{tag_id}")
async def remove_tag_from_dataset(dataset_id: str, tag_id: str, session: Session = Depends(db.get_session)):
    """
    Use this endpoint to remove a tag from a specific dataset
    """

    dataset = session.query(Dataset).filter(Dataset.id == dataset_id, Dataset.deleted_at == None).first()
    if not dataset:
        raise HTTPException(404)

    tag = session.query(Tag).filter(Tag.id == tag_id, Tag.deleted_at == None).first()
    if not tag:
        raise HTTPException(404)

    dataset.tags.remove(tag)
    session.commit()
    return dataset.to_dict()


@router.put("/{dataset_id}")
async def update_dataset(dataset_id: str, input: Dataset, session: Session = Depends(db.get_session)):
    """
    Use this endpoint to update a specific dataset
    """

    dataset = session.query(Dataset).filter(Dataset.id == dataset_id, Dataset.deleted_at == None).first()
    if not dataset:
        raise HTTPException(404)

    dataset.update(**input.model_dump(exclude=Dataset.get_ignored_fields()))
    session.commit()
    return dataset.to_dict()


@router.delete("/{dataset_id}")
async def delete_dataset(dataset_id: str, session: Session = Depends(db.get_session)):
    """
    Use this endpoint to delete a specific dataset
    """

    dataset = session.query(Dataset).filter(Dataset.id == dataset_id, Dataset.deleted_at == None).first()
    if not dataset:
        raise HTTPException(404)

    if dataset.deleted_at:
        raise HTTPException(404)
    dataset.update(deleted_at=datetime.now(timezone.utc), name=f"deleted_{dataset.name}")
    session.commit()
    return dataset.id