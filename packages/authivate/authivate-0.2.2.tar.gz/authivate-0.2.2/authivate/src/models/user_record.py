from dataclasses import dataclass, field
from datetime import datetime
from enum import  StrEnum
from typing import Dict

class UserStatusInProject(StrEnum):
    WAITLISTED = "waitlisted"
    INVITED = "invited"

    @staticmethod
    def from_string(user_status: str):
        user_status = user_status.lower()
        if user_status == 'invited':
            return UserStatusInProject.INVITED
        elif user_status == 'waitlisted':
            return UserStatusInProject.WAITLISTED
        else:
            raise ValueError(f"Unrecognized status: {user_status}")

    @property
    def is_waitlisted(self) -> bool:
        return self == UserStatusInProject.WAITLISTED

    @property
    def is_invited(self) -> bool:
        return self == UserStatusInProject.INVITED

@dataclass
class UserRecord:
    is_verified: bool
    date_created: datetime
    user_unique_id: str
    status_in_project: UserStatusInProject
    country_code: str
    country_name: str
    fields: Dict[str, any] = field(default_factory=dict)

    @staticmethod
    def from_json(json_data: Dict[str, any]) -> 'UserRecord':
        return UserRecord(
            is_verified=json_data['is_verified'],
            date_created=datetime.fromisoformat(json_data['date_created']),
            user_unique_id=json_data['user_unique_id'],
            status_in_project=UserStatusInProject.from_string(json_data['status_in_project']),
            country_code=json_data['country_code'],
            country_name=json_data['country_name'],
            fields=json_data.get('fields', {})
        )

    def to_json(self) -> Dict[str, any]:
        return {
            'is_verified': self.is_verified,
            'date_created': self.date_created.isoformat(),
            'user_unique_id': self.user_unique_id,
            'status_in_project': self.status_in_project.value,
            'country_code': self.country_code,
            'country_name': self.country_name,
            'fields': self.fields
        }
