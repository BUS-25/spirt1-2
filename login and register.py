from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Literal, Optional

Role = Literal["elderly", "carer"]


@dataclass
class User:
    id: str
    password: str
    name: str
    role: Role

    def verifyLogin(self, password_attempt: str) -> bool:
        return self.password == password_attempt


@dataclass
class Carer(User):
    carerID: int
    phoneNum: str


class Database:
    def __init__(self, path: str | Path = "users_db.json"):
        self.path = Path(path)
        self.connectionString: str = "local-json-db"
        self.dbStatus: bool = True

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
            data[user.id] = asdict(user)
            self._save(data)
            return True
        except Exception:
            return False

    def getUser(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self._load().get(user_id)


class AuthService:
    def __init__(self, db: Database):
        self.db = db

    def register_elderly(self, id: str, password: str, name: str) -> bool:
        id = id.strip()
        password = password.strip()
        name = name.strip()
        if not id or not password or not name:
            raise ValueError("Missing required fields")
        if self.db.userExists(id):
            raise ValueError("User already exists")
        user = User(id=id, password=password, name=name, role="elderly")
        if not self.db.saveUser(user):
            raise RuntimeError("Failed to save user")
        return True

    def register_carer(self, id: str, password: str, name: str, carerID: int, phoneNum: str) -> bool:
        id = id.strip()
        password = password.strip()
        name = name.strip()
        phoneNum = phoneNum.strip()
        if not id or not password or not name or not phoneNum:
            raise ValueError("Missing required fields")
        if carerID < 0:
            raise ValueError("Invalid carerID")
        if self.db.userExists(id):
            raise ValueError("User already exists")
        user = Carer(id=id, password=password, name=name, role="carer", carerID=carerID, phoneNum=phoneNum)
        if not self.db.saveUser(user):
            raise RuntimeError("Failed to save user")
        return True

    def login_elderly(self, id: str, password: str) -> Dict[str, Any]:
        return self._login(id=id, password=password, role="elderly")

    def login_carer(self, id: str, password: str) -> Dict[str, Any]:
        return self._login(id=id, password=password, role="carer")

    def _login(self, id: str, password: str, role: Role) -> Dict[str, Any]:
        id = id.strip()
        password = password.strip()
        if not id or not password:
            raise ValueError("Missing credentials")
        data = self.db.getUser(id)
        if not data:
            raise ValueError("User not found")
        if data.get("role") != role:
            raise ValueError("Role mismatch")
        user = User(id=data["id"], password=data["password"], name=data["name"], role=data["role"])
        if not user.verifyLogin(password):
            raise ValueError("Invalid password")
        return {
            "id": data.get("id"),
            "name": data.get("name"),
            "role": data.get("role"),
            "carerID": data.get("carerID"),
            "phoneNum": data.get("phoneNum"),
        }