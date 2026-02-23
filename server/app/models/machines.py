from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from .base import Base
from .enums import (
    ConditionEnum,
    ConditionEnumSA,
    CategoryEnum,
    CategoryEnumSA,
    VendorEnum,
    VendorEnumSA
)


class Machine(Base):
    __tablename__ = "machines"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    brand: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    serial: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    category: Mapped[CategoryEnum] = mapped_column(CategoryEnumSA, nullable=False)
    form_factor: Mapped[str] = mapped_column(String(100), nullable=False)
    
    color: Mapped[str] = mapped_column(String(50), nullable=False)
    condition: Mapped[ConditionEnum] = mapped_column(ConditionEnumSA, nullable=False)
    vendor: Mapped[VendorEnum] = mapped_column(VendorEnumSA, nullable=False, default=VendorEnum.UNKNOWN)
    
    #----------relationships--------------
    work_orders = relationship("WorkOrder", back_populates="machine", cascade="all, delete-orphan")
    work_order_events = relationship("WorkOrderEvent", back_populates="machine")
    notes = relationship("MachineNote", back_populates="machine")
    
    
    def serialize(self) -> dict:
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "serial": self.serial,
            "category": str(self.category),
            "form_factor": self.form_factor,
            "color": self.color,
            "condition": str(self.condition),
            "vendor": str(self.vendor)
        }
    