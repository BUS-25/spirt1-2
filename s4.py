from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Carer:
    id: str
    name: str
    phoneNum: str


@dataclass
class EmergencyAlert:
    alert_id: int
    elderly_id: str
    carer_id: str
    timestamp: str
    status: str


class Database:
    def __init__(self, carers_path: str | Path = "carers.json", alerts_path: str | Path = "emergency_alerts.json"):
        self.carers_path = Path(carers_path)
        self.alerts_path = Path(alerts_path)
        self.connectionString: str = "local-json-db"
        self.dbStatus: bool = True

    def _load_json(self, path: Path) -> Any:
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))

    def _save_json(self, path: Path, data: Any) -> None:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def saveCarer(self, carer: Carer) -> bool:
        try:
            data = self._load_json(self.carers_path