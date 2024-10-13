import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from api.deps import (
    CurrentUser,
    SessionDep,
)
from models import (
    Collection,
    CollectionCreate, 
    CollectionPublic, 
    CollectionsPublic, 
    CollectionUpdate, 
    Message
)

router = APIRouter()


@router.get("/me", response_model=CollectionsPublic)
async def get_next_collections(
    *, session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Get the next bin collections for the user
    """
    collections = session.exec(select(Collection).where(Collection.user_id == current_user.id))
    return collections


@router.get("/{user_id}", response_model=CollectionsPublic)
async def get_collections(
    *, session: SessionDep, user_id: uuid.UUID, current_user: CurrentUser
) -> Any:
    """
    Get all collections for a user
    """
    collections = session.exec(select(Collection).where(Collection.user_id == user_id))
    return collections


@router.get("/{collection_id}", response_model=CollectionPublic)
async def get_collection(
    *, session: SessionDep, collection_id: uuid.UUID, current_user: CurrentUser
) -> Any:
    """
    Get a collection by id
    """
    collection = session.get(Collection, collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@router.post("/", response_model=CollectionPublic)
async def create_collection(
    *, session: SessionDep, collection_in: CollectionCreate
) -> Any:
    """
    Create a new collection
    """
    collection = Collection.from_orm(collection_in)
    session.add(collection)
    session.commit()
    session.refresh(collection)
    return collection


@router.patch("/{collection_id}", response_model=CollectionPublic)
async def update_collection(
    *, session: SessionDep, collection_id: uuid.UUID, collection_in: CollectionUpdate, current_user: CurrentUser
) -> Any:
    """
    Update a collection
    """
    collection = session.get(Collection, collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    collection_data = collection_in.dict(exclude_unset=True)
    for key, value in collection_data.items():
        setattr(collection, key, value)
    session.add(collection)
    session.commit()
    session.refresh(collection)
    return collection


@router.delete("/{collection_id}", response_model=Message)
async def delete_collection(
    *, session: SessionDep, collection_id: uuid.UUID, current_user: CurrentUser
) -> Any:
    """
    Delete a collection
    """
    collection = session.get(Collection, collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    session.delete(collection)
    session.commit()
    return {"message": "Collection deleted"}

