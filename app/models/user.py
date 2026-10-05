from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from werkzeug.security import check_password_hash


@dataclass
class User:
    """
    Domain entity representing a user in the drug prevention community platform.
    Includes encapsulation, basic validation, and role identification.
    """
    id: Optional[int]
    username: str
    email: str
    password_hash: str
    full_name: str
    role: str = "USER"  # 'USER', 'CONSULTANT', 'ADMIN'
    phone: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        self.validate()

    def validate(self) -> None:
        """Basic domain invariant validation."""
        if not self.username or len(self.username.strip()) < 3:
            raise ValueError("Tên đăng nhập phải có ít nhất 3 ký tự.")
        if not self.email or "@" not in self.email:
            raise ValueError("Email không hợp lệ.")
        if self.role.upper() not in ("USER", "CONSULTANT", "ADMIN", "GUEST"):
            raise ValueError(f"Vai trò '{self.role}' không hợp lệ trong hệ thống.")
        self.role = self.role.upper()

    def verify_password(self, password: str) -> bool:
        """Verifies plaintext password against stored hash."""
        return check_password_hash(self.password_hash, password)

    def is_admin(self) -> bool:
        return self.role == "ADMIN"

    def is_consultant(self) -> bool:
        return self.role == "CONSULTANT"

    def is_user(self) -> bool:
        return self.role == "USER"

