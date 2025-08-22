import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
import uuid
import datetime


class TaskStatus(Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = 'tasks'
    
    uuid = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    description: Mapped[str] = mapped_column(sa.Text, nullable=True)
    status: Mapped[Enum] = mapped_column(
        sa.Enum('created', 'in_progress', 'completed', name="task_status", native_enum=True),
        default=TaskStatus.CREATED,
        nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(sa.DateTime, default=datetime.datetime.now, nullable=False)

    __table_args__ = (
        sa.UniqueConstraint('name', name='uq_name'), )