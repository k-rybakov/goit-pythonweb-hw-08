from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.contacts import ContactRepository
from src.schemas import ContactCreate, ContactUpdate
from src.database.models import Contact


class ContactService:
    def __init__(self, db: AsyncSession):
        self.repository = ContactRepository(db)

    async def get_contacts(self, skip: int = 0, limit: int = 100) -> List[Contact]:
        return await self.repository.get_contacts(skip, limit)

    async def get_contact(self, contact_id: int) -> Optional[Contact]:
        return await self.repository.get_contact_by_id(contact_id)

    async def create_contact(self, contact: ContactCreate) -> Contact:
        return await self.repository.create_contact(contact)

    async def update_contact(
        self, contact_id: int, contact: ContactUpdate
    ) -> Optional[Contact]:
        return await self.repository.update_contact(contact_id, contact)

    async def delete_contact(self, contact_id: int) -> Optional[Contact]:
        return await self.repository.delete_contact(contact_id)

    async def search_contacts(
        self, first_name: str = None, last_name: str = None, email: str = None
    ) -> List[Contact]:
        return await self.repository.search_contacts(first_name, last_name, email)

    async def get_contacts_with_upcoming_birthdays(self) -> List[Contact]:
        return await self.repository.get_contacts_with_upcoming_birthdays()
