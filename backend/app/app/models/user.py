from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.schemas.repetition import Repetition
from .user_deck import user_deck

if TYPE_CHECKING:
    from .suspended import Suspended  # noqa: F401
    from .history import History  # noqa: F401
    from .deck import Deck  # noqa: F401
    from .fact import Fact  # noqa: F401


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True, nullable=False)
    is_superuser = Column(Boolean(), default=False, nullable=False)
    repetition_model = Column(Enum(Repetition), default=Repetition.leitner, nullable=False)
    default_deck_id = Column(Integer, ForeignKey("deck.id"), default=1)

    default_deck = relationship("Deck", foreign_keys=default_deck_id)
    decks = relationship("Deck", secondary=user_deck, back_populates="users")
    history = relationship("History", back_populates="user")
    suspended_facts = association_proxy('suspended', 'suspended_fact')
