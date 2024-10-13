import uuid
from datetime import datetime
from enum import Enum
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
    
     
class PreferredContactMethod(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    
class ReminderTime(str, Enum):
    ONE_HOUR = "1_hour"
    TWO_HOURS = "2_hours"
    TWELVE_HOURS = "12_hours"
    TWENTY_FOUR_HOURS = "24_hours"
    FOURTY_EIGHT_HOURS = "48_hours"
    
class BinType(str, Enum):
    HOUSEHOLD_WASTE = "household_waste"
    RECYCLING = "recycling"
    GARDEN_WASTE = "garden_waste"
    
    
# --------------------------- USERS ---------------------------
class UserBase(SQLModel):
    name: str = Field(..., nullable=False, max_length=255)
    email: EmailStr = Field(..., nullable=False, unique=True, max_length=255)
    phone_number: str | None = Field(default=None, nullable=True, max_length=15)
    preferred_contact_method: PreferredContactMethod = Field(default=PreferredContactMethod.EMAIL, nullable=False)
    address: str = Field(default=None, nullable=False, max_length=255)
    collection_url: str | None = Field(default=None, nullable=True, max_length=511)
    reminder_time: ReminderTime = Field(default=ReminderTime.TWENTY_FOUR_HOURS, nullable=False)
    is_active: bool = True

    
class UserCreate(UserBase):
    password: str = Field(..., nullable=False, min_length=8, max_length=255)
    

class UserRegister(UserBase):   
    password: str = Field(..., nullable=False, min_length=8, max_length=255)
    
    
class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=255)
    new_password: str = Field(min_length=8, max_length=255)
    
    
class UserUpdate(UserBase):
    name: str | None = Field(default=None, nullable=True, max_length=255)
    email: EmailStr | None = Field(default=None, nullable=True, max_length=255)
    phone_number: str | None = Field(default=None, nullable=True, max_length=15)
    preferred_contact_method: PreferredContactMethod | None = Field(default=None, nullable=True)
    address: str | None = Field(default=None, nullable=True, max_length=255)
    collection_url: str | None = Field(default=None, nullable=True, max_length=511)
    reminder_time: ReminderTime | None = Field(default=None, nullable=True)
    password: str | None = Field(default=None, nullable=True, min_length=8, max_length=255)
    
    
class UserUpdateMe(UserBase):
    name: str | None = Field(default=None, nullable=True, max_length=255)
    email: EmailStr | None = Field(default=None, nullable=True, max_length=255)
    phone_number: str | None = Field(default=None, nullable=True, max_length=15)
    preferred_contact_method: PreferredContactMethod | None = Field(default=None, nullable=True)
    address: str | None = Field(default=None, nullable=True, max_length=255)
    collection_url: str | None = Field(default=None, nullable=True, max_length=511)
    reminder_time: ReminderTime | None = Field(default=None, nullable=True)
    
    
class User(UserBase, table=True):
    id: uuid.UUID = Field(default=uuid.uuid4(), primary_key=True)
    hashed_password: str 
    
    collection_url: str | None = Field(default=None, nullable=True, max_length=511)
    next_scrape_date: datetime = Field(default=datetime.now(), nullable=False)
    
    collections: list["Collection"] = Relationship(back_populates="user", cascade_delete=True)
        

class UserPublic(UserBase):
    id: uuid.UUID
    collection_url: str
    next_scrape_date: datetime
    

class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
    
    
# --------------------------- COLLECTIONS ---------------------------

class CollectionBase(SQLModel):
    bin_type: BinType = Field(..., nullable=False)
    collection_date: datetime = Field(..., nullable=False)
    notification_sent: bool = Field(default=False, nullable=False)
    

class CollectionCreate(CollectionBase):
    pass


class CollectionUpdate(CollectionBase):
    bin_type: BinType | None = Field(default=None, nullable=True)
    collection_date: datetime | None = Field(default=None, nullable=True)
    notification_sent: bool | None = Field(default=None, nullable=True)
        
        
class Collection(CollectionBase, table=True):
    id: uuid.UUID = Field(default=uuid.uuid4(), primary_key=True)
    user_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    user: User | None = Relationship(back_populates="collections")


class CollectionPublic(CollectionBase):
    id: uuid.UUID
    user_id: uuid.UUID
    

class CollectionsPublic(SQLModel):
    data: list[CollectionPublic]
    count: int
    

# --------------------------- TOKENS ---------------------------
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
    

class TokenPayload(SQLModel):
    sub: str | None = None
    

# --------------------------- MISC ---------------------------
class Message(SQLModel):
    message: str