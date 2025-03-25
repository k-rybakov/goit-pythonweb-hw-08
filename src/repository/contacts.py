from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Contact
from src.schemas import ContactCreate, ContactUpdate


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(self, skip: int = 0, limit: int = 100) -> List[Contact]:
        stmt = select(Contact).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_contact_by_id(self, contact_id: int) -> Optional[Contact]:
        stmt = select(Contact).where(Contact.id == contact_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_contact(self, contact: ContactCreate) -> Contact:
        new_contact = Contact(**contact.dict())
        self.db.add(new_contact)
        await self.db.commit()
        await self.db.refresh(new_contact)
        return new_contact

    async def update_contact(
        self, contact_id: int, contact: ContactUpdate
    ) -> Optional[Contact]:
        stmt = (
            update(Contact)
            .where(Contact.id == contact_id)
            .values(**contact.dict(exclude_unset=True))
            .execution_options(synchronize_session="fetch")
        )
        await self.db.execute(stmt)
        await self.db.commit()
        return await self.get_contact_by_id(contact_id)

    async def delete_contact(self, contact_id: int) -> Optional[Contact]:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def search_contacts(
        self, first_name: str = None, last_name: str = None, email: str = None
    ) -> List[Contact]:
        stmt = select(Contact)
        if first_name:
            stmt = stmt.where(Contact.first_name.ilike(f"%{first_name}%"))
        if last_name:
            stmt = stmt.where(Contact.last_name.ilike(f"%{last_name}%"))
        if email:
            stmt = stmt.where(Contact.email.ilike(f"%{email}%"))
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_contacts_with_upcoming_birthdays(self) -> List[Contact]:
        from datetime import date, timedelta

        today = date.today()
        end_date = today + timedelta(days=7)
        # Проста реалізація: припустимо, що день народження зберігається з актуальним роком
        stmt = select(Contact).where(Contact.birthday.between(today, end_date))
        result = await self.db.execute(stmt)
        return result.scalars().all()
