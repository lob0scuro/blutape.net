from app.extensions import db
from sqlalchemy import Column, Text, String, Integer, Boolean, Enum, Date, DateTime, ForeignKey, func, case, and_
from sqlalchemy.orm import relationship
from flask_login import UserMixin

TypeEnum = Enum("fridge", "washer", "dryer", "range", "microwave", "water_heater", "stackable", "dishwasher")
ConditionEnum = Enum("NEW", "USED", "Scratch and Dent", name="condition_enum")
VendorEnum = Enum("pasadena", "baton_rouge", "alexandria", "stines_lc", "stines_jn", "scrappers", "viking", "unknown", name="vendor_enum")
StatusEnum = Enum("completed", "trashed", "in_progress", "exported", "archived", name="status_enum")
RoleEnum = Enum("office", "fridge_tech", "washer_tech", "dryer_range_tech", "inventory")



# -----------------------
#       USERS
# -----------------------
class Users(db.Model, UserMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    role = Column(RoleEnum, nullable=False)
    is_admin = Column(Boolean, default=False)
    email = Column(String(150), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    
    machines = relationship("Machines", back_populates="technician", lazy=True)
    machine_notes = relationship("Notes", back_populates="author", lazy=True, cascade="all, delete-orphan")
    
    
    #-----------------------
    #    HELPER METHODS
    #-----------------------
    def stats(self, statuses=None, start_date=None, end_date=None, date_column="started_on"):
        from app.models import Machines
        from datetime import datetime, date
        
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            
        query = Machines.query.filter(Machines.technician_id == self.id)
        
        if start_date and end_date:
            query = query.filter(getattr(Machines, date_column).between(start_date, end_date))
        elif start_date:
            query = query.filter(getattr(Machines, date_column) >= start_date)
        elif end_date:
            query = query.filter(getattr(Machines, date_column) <= end_date)
            
        if statuses:
            query = query.filter(Machines.status.in_(statuses))
            
        machines = query.all()
        
        result = {}
        for m in machines:
            result.setdefault(m.status, {"count": 0, "machines": []})
            result[m.status]["count"] += 1
            result[m.status]["machines"].append(m.serialize())
            
        for status in ["in_progress", "completed", "trashed"]:
            result.setdefault(status, {"count": 0, "machines": []})
            
        return result
    
    
    
    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role,
            "is_admin": self.is_admin,
            "email": self.email,
        }
        
        
# -----------------------
#       MACHINES
# -----------------------
class Machines(db.Model):
    __tablename__ = "machines"
    
    id = Column(Integer, primary_key=True)
    brand = Column(String(50), nullable=False)
    type_of = Column(TypeEnum, nullable=False)
    model = Column(String(100), nullable=False)
    serial = Column(String(150), nullable=False, unique=True)
    style = Column(String(50), nullable=False)
    color = Column(String(50), nullable=False)
    condition = Column(ConditionEnum, nullable=False)
    vendor = Column(VendorEnum)
    status = Column(StatusEnum, default="in_progress", nullable=False)
    
    started_on = Column(Date, nullable=False)
    completed_on = Column(Date, nullable=True)
    trashed_on = Column(Date, nullable=True)
    exported_on = Column(Date, nullable=True)
    
    technician_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    technician = relationship("Users", back_populates="machines")
    notes = relationship("Notes", back_populates="machine", cascade="all, delete-orphan")
    
    def serialize(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "type_of": self.type_of,
            "model": self.model,
            "serial": self.serial,
            "style": self.style,
            "color": self.color,
            "condition": self.condition,
            "vendor": self.vendor,
            "status": self.status,
            "started_on": self.started_on,
            "completed_on": self.completed_on,
            "trashed_on": self.trashed_on,
            "exported_on": self.exported_on,
            "tech_id": self.technician_id,
            "tech_name": f"{self.technician.first_name} {self.technician.last_name}",            
            "notes": [n.serialize() for n in self.notes]
        }
        
        
# -----------------------
#       NOTES
# -----------------------    
class Notes(db.Model):
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    date = Column(Date, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    machine_id = Column(Integer, ForeignKey("machines.id", ondelete="SET NULL"))
    
    author = relationship("Users", back_populates="machine_notes")
    machine = relationship("Machines", back_populates="notes")
    
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "date": self.date,
            "user_id": self.user_id,
            "machine_id": self.machine_id,
            "author_name": f"{self.author.first_name} {self.author.last_name}" if self.author else None,
            "machine_serial": self.machine.serial if self.machine else None
        }