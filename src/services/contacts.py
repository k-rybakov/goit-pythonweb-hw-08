from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.contacts import ContactRepository
from src.schemas import ContactCreate, ContactUpdate
from src.database.models import Contact, User
from sqlalchemy.exc import IntegrityError


class ContactService:
    def __init__(self, db: AsyncSession):
        self.repository = ContactRepository(db)

    async def get_contacts(
        self, user: User, skip: int = 0, limit: int = 100
    ) -> List[Contact]:
        return await self.repository.get_contacts(user, skip, limit)

    async def get_contact(self, contact_id: int, user: User) -> Optional[Contact]:
        return await self.repository.get_contact_by_id(contact_id, user)

    async def create_contact(self, body: ContactCreate, user: User) -> Contact:
        try:
            return await self.repository.create_contact(body, user)
        except IntegrityError as e:
            # You can further inspect the exception string if needed
            if "contacts_email_key" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Contact with this email already exists",
                )
            raise

    async def update_contact(
        self, contact_id: int, body: ContactUpdate, user: User
    ) -> Optional[Contact]:
        return await self.repository.update_contact(contact_id, body, user)

    async def delete_contact(self, contact_id: int, user: User) -> Optional[Contact]:
        return await self.repository.delete_contact(contact_id, user)

    async def search_contacts(
        self,
        user: User,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
    ) -> List[Contact]:
        return await self.repository.search_contacts(user, first_name, last_name, email)

    async def get_contacts_with_upcoming_birthdays(self, user: User) -> List[Contact]:
        return await self.repository.get_contacts_with_upcoming_birthdays(user)
