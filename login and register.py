from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Literal, Optional

Role = Literal["elderly", "carer"]


@dataclass
class User:
    user_id: str
    password: str
    name: str
    role: Role

    def verifyLogin(self, password_attempt: str) -> bool:
        return self.password == password_attempt


@dataclass
class ElderlyUser(User):
    age_range: str


@dataclass
class Carer(User):
    phone: str = ""


class Database:
    def __init__(self, path: str | Path = "users_auth.json"):
        self.path = Path(path)
        self.connectionString = "local-json-db"
        self.dbStatus = True

    def _load(self) -> Dict[str, Any]:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _save(self, data: Dict[str, Any]) -> None:
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def userExists(self, user_id: str) -> bool:
        return user_id in self._load()

    def saveUser(self, user: User) -> bool:
        try:
            data = self._load()
            data[user.user_id] = asdict(user)
            self._save(data)
            return True
        except Exception:
            return False

    def getUser(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self._load().get(user_id)


class AuthService:
    def __init__(self, db: Database):
        self.db = db

    def register_elderly(self, user_id: str, password: str, name: str, age_range: str) -> bool:
        user_id = user_id.strip()
        name = name.strip()
        password = password.strip()
        age_range = age_range.strip()
        if not user_id or not name or not password or not age_range:
            raise ValueError("Missing required fields")
        if self.db.userExists(user_id):
            raise ValueError("User ID already exists")
        user = ElderlyUser(user_id=user_id, password=password, name=name, role="elderly", age_range=age_range)
        ok = self.db.saveUser(user)
        if not ok:
            raise RuntimeError("Failed to save user")
        return True

    def register_carer(self, user_id: str, password: str, name: str, phone: str = "") -> bool:
        user_id = user_id.strip()
        name = name.strip()
        password = password.strip()
        phone = phone.strip()
        if not user_id or not name or not password:
            raise ValueError("Missing required fields")
        if self.db.userExists(user_id):
            raise ValueError("User ID already exists")
        user = Carer(user_id=user_id, password=password, name=name, role="carer", phone=phone)
        ok = self.db.saveUser(user)
        if not ok:
            raise RuntimeError("Failed to save user")
        return True

    def login_elderly(self, user_id: str, password: str, age_range: str) -> Dict[str, Any]:
        return self._login(user_id=user_id, password=password, role="elderly", age_range=age_range)

    def login_carer(self, user_id: str, password: str) -> Dict[str, Any]:
        return self._login(user_id=user_id, password=password, role="carer", age_range=None)

    def _login(self, user_id: str, password: str, role: Role, age_range: Optional[str]) -> Dict[str, Any]:
        user_id = user_id.strip()
        password = password.strip()
        if not user_id or not password:
            raise ValueError("Missing credentials")

        data = self.db.getUser(user_id)
        if not data:
            raise ValueError("User not found")

        if data.get("role") != role:
            raise ValueError("Role mismatch")

        user = User(user_id=data["user_id"], password=data["password"], name=data["name"], role=data["role"])
        if not user.verifyLogin(password):
            raise ValueError("Invalid password")

        if role == "elderly":
            if not age_range or not age_range.strip():
                raise ValueError("Missing age range")
            stored_age = data.get("age_range")
            if stored_age and stored_age != age_range.strip():
                raise ValueError("Age range mismatch")

        return {
            "user_id": data.get("user_id"),
            "name": data.get("name"),
            "role": data.get("role"),
            "age_range": data.get("age_range"),
            "phone": data.get("phone"),
        }