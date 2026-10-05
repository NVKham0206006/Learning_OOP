"""User service — register, authenticate, profile."""
from typing import Optional, List
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository = None):
        self.user_repo = user_repo or UserRepository()

    def register(self, username: str, email: str, password: str,
                 full_name: str, phone: str = None) -> User:
        """Đăng ký user mới với password đã hash."""
        username = (username or "").strip()
        email = (email or "").strip().lower()
        full_name = (full_name or "").strip()

        if not username or len(username) < 3:
            raise ValueError("Tên đăng nhập phải có ít nhất 3 ký tự.")
        if not email or "@" not in email:
            raise ValueError("Email không hợp lệ.")
        if not password or len(password) < 6:
            raise ValueError("Mật khẩu phải có ít nhất 6 ký tự.")
        if not full_name:
            raise ValueError("Họ tên không được để trống.")

        if self.user_repo.get_by_username(username):
            raise ValueError("Tên đăng nhập đã tồn tại.")
        if self.user_repo.get_by_email(email):
            raise ValueError("Email đã được sử dụng.")

        user = User(
            id=None,
            username=username,
            email=email,
            password_hash=generate_password_hash(password, method="scrypt"),
            full_name=full_name,
            role="USER",
            phone=phone,
        )
        user_id = self.user_repo.create(user)
        user.id = user_id
        return user

    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Kiểm tra credentials. Trả về User nếu hợp lệ, None nếu không."""
        if not username or not password:
            return None
        user = self.user_repo.get_by_username(username.strip())
        if not user:
            return None
        if not user.is_active:
            return None
        if not user.verify_password(password):
            return None
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.user_repo.get_by_id(user_id)

    def update_profile(self, user_id: int, full_name: str, email: str,
                       phone: str = None) -> bool:
        if not full_name or not full_name.strip():
            raise ValueError("Họ tên không được để trống.")
        if not email or "@" not in email:
            raise ValueError("Email không hợp lệ.")
        return self.user_repo.update_profile(user_id, full_name.strip(),
                                              email.strip().lower(), phone)

    def list_all(self, role: str = None) -> List[User]:
        if role:
            return self.user_repo.get_all_by_role(role)
        return self.user_repo.get_all()