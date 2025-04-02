from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User
from src.services.auth import get_current_user
from src.database.db import get_db
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from src.services.contacts import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    skip: int = 0,
    limit: int = 100,
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ContactService(db)
    if first_name or last_name or email:
        contacts = await service.search_contacts(user, first_name, last_name, email)
    else:
        contacts = await service.get_contacts(user, skip, limit)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ContactService(db)
    contact = await service.get_contact(contact_id, user)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    contact: ContactCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ContactService(db)
    return await service.create_contact(contact, user)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ContactService(db)
    updated = await service.update_contact(contact_id, contact, user)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return updated


@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ContactService(db)
    deleted = await service.delete_contact(contact_id, user)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return deleted


@router.get("/birthdays/upcoming", response_model=List[ContactResponse])
async def get_upcoming_birthdays(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service = ContactService(db)
    contacts = await service.get_contacts_with_upcoming_birthdays(user)
    return contacts
