from datetime import datetime

from sqlalchemy import Boolean, BigInteger, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database.base import Base


class User(Base):
    __tablename__ = 'users'

    chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    username: Mapped[str] = mapped_column(String(34), nullable=True)
    fullname: Mapped[str] = mapped_column(String(255), nullable=True)

    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_subscribed: Mapped[bool] = mapped_column(Boolean, default=True)
    is_promoted: Mapped[bool] = mapped_column(Boolean, default=True)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)

    push1: Mapped[bool] = mapped_column(Boolean, default=False)
    push5: Mapped[bool] = mapped_column(Boolean, default=True)
    push10: Mapped[bool] = mapped_column(Boolean, default=False)
    push30: Mapped[bool] = mapped_column(Boolean, default=False)

    notifications: Mapped[list["Notification"]] = relationship(
        "Notification", back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )


class Notification(Base):
    __tablename__ = 'notification'

    chat_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.chat_id'), primary_key=True, nullable=False)
    boss_id: Mapped[int] = mapped_column(Integer, ForeignKey('bosses.id'), primary_key=True, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="notifications")
    boss: Mapped["Boss"] = relationship("Boss", back_populates="notifications")


class Boss(Base):
    __tablename__ = 'bosses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    boss_day: Mapped[int] = mapped_column(Integer)
    boss_time: Mapped[str] = mapped_column(String)
    boss_names: Mapped[str] = mapped_column(String)
    boss_slot: Mapped[str] = mapped_column(String)

    notifications: Mapped[list["Notification"]] = relationship(
        "Notification", back_populates="boss", cascade="all, delete-orphan", passive_deletes=True
    )

    def __repr__(self):
        return f"Boss(id={self.id}, boss_day={self.boss_day}, boss_time={self.boss_time}, boss_names={self.boss_names})"


class PromoCode(Base):
    __tablename__ = 'promo_codes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(50))
    loot: Mapped[str] = mapped_column(String(255))
    expiry: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    owner: Mapped[str] = mapped_column(String(50))
