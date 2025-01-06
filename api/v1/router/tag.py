from fastapi import APIRouter, Depends, HTTPException
from core import db, Session
from schema import Tag
from datetime import datetime, timezone


router = APIRouter()


@router.post("/")
async def create_tag(input: Tag, session: Session = Depends(db.get_session)):
    """
    Use this endpoint to create a new tag
    """
    tag = Tag(**input.model_dump(exclude=Tag.get_ignored_fields()))

    try:
        session.add(tag)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(400)
    return tag.to_dict()


@router.get("/")
async def get_all_tags(session: Session = Depends(db.get_session)):
    """
    Use this endpoint to get all tags
    """

    tags = session.query(Tag).filter(Tag.deleted_at == None).all()
    return [tag.to_dict() for tag in tags]


@router.get("/search")
async def search_tags(name: str = None, session: Session = Depends(db.get_session)):
    """
    Use this endpoint to search tags
    """

    tags = session.query(Tag).filter(Tag.name.ilike(f"%{name}%"), Tag.deleted_at == None)
    return [tag.to_dict() for tag in tags.all()]


@router.get("/{tag_id}")
async def get_tag(tag_id: str, session: Session = Depends(db.get_session)):
    """
    Use this endpoint to get a specific tag
    """

    tag = session.query(Tag).filter(Tag.id == tag_id, Tag.deleted_at == None).first()
    if not tag:
        raise HTTPException(404)
    return tag.to_dict()


@router.put("/{tag_id}")
async def update_tag(tag_id: str, input: Tag, session: Session = Depends(db.get_session)):
    """
    Use this endpoint to update a specific tag
    """

    tag = session.query(Tag).filter(Tag.id == tag_id, Tag.deleted_at == None).first()
    if not tag:
        raise HTTPException(404)

    tag.update(**input.model_dump(exclude=Tag.get_ignored_fields()))
    session.commit()
    return tag.to_dict()


@router.delete("/{tag_id}")
async def delete_tag(tag_id: str, session: Session = Depends(db.get_session)):
    """
    Use this endpoint to delete a specific tag
    """

    tag = session.query(Tag).filter(Tag.id == tag_id, Tag.deleted_at == None).first()
    if not tag:
        raise HTTPException(404)

    if tag.deleted_at:
        raise HTTPException(404)
    tag.update(deleted_at=datetime.now(timezone.utc))
    session.commit()
    return tag.id