from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, Date
from .base import Base
from .enums import EventEnum, EventEnumSA, EventReasonEnum, EventReasonEnumSA, StatusEnum, StatusEnumSA
from datetime import date as DTdate


class WorkOrderEvent(Base):
    __tablename__ = "work_order_events"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    work_order_id: Mapped[int] = mapped_column(Integer, ForeignKey("work_orders.id"), nullable=False)
    machine_id: Mapped[int] = mapped_column(Integer, ForeignKey("machines.id"), nullable=False)
    event_type: Mapped[EventEnum] = mapped_column(EventEnumSA, nullable=False, default=EventEnum.INITIATED)
    from_status: Mapped[StatusEnum] = mapped_column(StatusEnumSA, nullable=True)
    to_status: Mapped[StatusEnum] = mapped_column(StatusEnumSA, nullable=True)
    
    event_date: Mapped[DTdate] = mapped_column(Date, nullable=False, default=DTdate.today)
    technician_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    
    reason: Mapped[EventReasonEnum] = mapped_column(EventReasonEnumSA, nullable=True, default=EventReasonEnum.DEFAULT)
    
    
    #----------relationships--------------
    work_order = relationship("WorkOrder", back_populates="events")
    machine = relationship("Machine", back_populates="work_order_events")
    technician = relationship("User", back_populates="work_order_events", foreign_keys=[technician_id])
    
    
    def serialize(self) -> dict:
        return {
            "id": self.id,
            "work_order_id": self.work_order_id,
            "machine_id": self.machine_id,
            "event_type": str(self.event_type),
            "from_status": str(self.from_status),
            "to_status": str(self.to_status),
            "event_date": self.event_date.strftime("%Y-%m-%d"),
            "technician_id": self.technician_id,
            "reason": str(self.reason)
        }