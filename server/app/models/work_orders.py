from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Date, ForeignKey
from .base import Base
from .enums import StatusEnum, StatusEnumSA
from datetime import date as DTdate

class WorkOrder(Base):
    __tablename__ = "work_orders"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    machine_id: Mapped[int] = mapped_column(ForeignKey("machines.id"), nullable=False)
    
    initiated_on: Mapped[DTdate] = mapped_column(Date, nullable=False, default=DTdate.today)
    initiated_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    current_status: Mapped[StatusEnum] = mapped_column(StatusEnumSA, nullable=False, default=StatusEnum.IN_PROGRESS)
    
    closed_on: Mapped[DTdate] = mapped_column(Date, nullable=True)
    archived_on: Mapped[DTdate] = mapped_column(Date, nullable=True)
    
    
    #----------relationships--------------
    machine = relationship("Machine", back_populates="work_orders")
    initiator = relationship("User", back_populates="initiated_work_orders", foreign_keys=[initiated_by])
    events = relationship("WorkOrderEvent", back_populates="work_order", cascade="all, delete-orphan")
    
    def serialize(self) -> dict:
        return {
            "id": self.id,
            "machine_id": self.machine_id,
            "initiated_on": self.initiated_on.strftime("%Y-%m-%d"),
            "initiator": {
                "id": self.initiator.id,
                "first_name": self.initiator.first_name,
                "last_name": self.initiator.last_name,
            },
            "current_status": str(self.current_status),
            "closed_on": self.closed_on.strftime("%Y-%m-%d") if self.closed_on
             else None,
            "archived_on": self.archived_on.strftime("%Y-%m-%d") if self.archived_on else None
        }