from sqlalchemy import Column, DateTime, Boolean, func

class AuditMixin:
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp()
    )

    modificated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    habilited = Column(
        Boolean,
        nullable=False,
        server_default="1"
    )

    deleted_at = Column(
        DateTime,
        nullable=True
    )