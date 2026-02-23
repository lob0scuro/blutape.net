from enum import Enum
from sqlalchemy import Enum as SAEnum

class RoleEnum(str, Enum):
    TECHNICIAN = "technician"
    ADMIN = "admin"
    
    def __str__(self):
        return self.value
    
RoleEnumSA = SAEnum(
    RoleEnum,
    name="role_enum",
    native_enum=False,
    validate_strings=True
)


class StatusEnum(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    TRASHED = "trashed"
    ARCHIVED = "archived"
    
    def __str__(self):
        return self.value
    
StatusEnumSA = SAEnum(
    StatusEnum,
    name="status_enum",
    native_enum=False,
    validate_strings=True
)


class EventEnum(str, Enum):
    INITIATED = "initiated"
    COMPLETED = "completed"
    TRASHED = "trashed"
    REOPENED = "reopened"
    ARCHIVED = "archived"
    UNARCHIVED = "unarchived"
    
    def __str__(self):
        return self.value
    
EventEnumSA = SAEnum(
    EventEnum,
    name="event_enum",
    native_enum=False,
    validate_strings=True
)


class EventReasonEnum(str, Enum):
    DEFAULT = "default"
    WARRANTY = "warranty"
    RETURN = "return"
    
    def __str__(self):
        return self.value
    

EventReasonEnumSA = SAEnum(
    EventReasonEnum,
    name="event_reason_enum",
    native_enum=False,
    validate_strings=True
)


class VendorEnum(str, Enum):
    PASADENA = "pasadena"
    BATON_ROUGE = "baton_rouge"
    ALEXANDRIA = "alexandria"
    STINES = "stines"
    SCRAPPERS = "scrappers"
    VIKING = "viking"
    UNKNOWN = "unknown"
    
    def __str__(self):
        return self.value
    
    
VendorEnumSA = SAEnum(
    VendorEnum,
    name="vendor_enum",
    native_enum=False,
    validate_strings=True
)


class ConditionEnum(str, Enum):
    NEW = "new"
    USED = "used"
    SCRATCH_AND_DENT = "scratch_and_dent"
    
    def __str__(self):
        return self.value
    
ConditionEnumSA = SAEnum(
    ConditionEnum,
    name="condition_enum",
    native_enum=False,
    validate_strings=True
)


class CategoryEnum(str, Enum):
    REFRIGERATOR = "refrigerator"
    WASHER = "washer"
    DRYER = "dryer"
    RANGE = "range"
    OVEN = "oven"
    MICROWAVE = "microwave"
    WATER_HEATER = "water_heater"
    LAUNDRY_TOWER = "laundry_tower"
    DISHWASHER = "dishwasher"
    
    def __str__(self):
        return self.value
    
CategoryEnumSA = SAEnum(
    CategoryEnum,
    name="type_enum",
    native_enum=False,
    validate_strings=True
)