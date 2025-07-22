import enum

class UserRole(str, enum.Enum):
    ADMIN = 'admin'
    USER = 'user'

class EmailType(str, enum.Enum):
    SMTP = 'smtp'
    MSAL = 'msal'

class FrequencyType(str, enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"