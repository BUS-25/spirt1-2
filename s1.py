from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Callable, List, Literal, Optional

Category = Literal["medication", "activity"]


@dataclass
class Reminder:
    category: Category
    name: str
    time_hhmm: str
    enabled: bool = True
    frequency: str = "daily"
    icon: str = ""
    last_alert_date: Optional[str] = None

    def validate(self) -> None:
        if self.category not in ("medication", "activity"):
            raise ValueError("Invalid category")
        if not self.name.strip():
            raise ValueError("Name is required")
        datetime.strptime(self.time_hhmm, "%H:%M")

    def is_due(self, now: datetime) -> bool:
        if not self.enabled:
            return False
        if now.strftime("%H:%M") != self.time_hhmm:
            return False
        today = now.strftime("%Y-%m-%d")
        return self.last_alert_date != today

    def mark_alerted(self, now: datetime) -> None:
        self.last_alert_date = now.strftime("%Y-%m-%d")


class ReminderStore:
    def __init__(self, path: str | Path = "reminders.json"):
        self.path = Path(path)

    def load(self) -> List[Reminder]:
        if not self.path.exists():
            return []
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        items: List[Reminder] = []
        for obj in raw:
            r = Reminder(**obj)
            r.validate()
            if not r.icon:
                r.icon = "💊" if r.category == "medication" else "🏃"
            items.append(r)
        return items

    def save(self, reminders: List[Reminder]) -> None:
        for r in reminders:
            r.validate()
            if not r.icon:
                r.icon = "💊" if r.category == "medication" else "🏃"
        self.path.write_text(
            json.dumps([asdict(r) for r in reminders], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def add(self, reminder: Reminder) -> List[Reminder]:
        reminders = self.load()
        reminder.validate()
        if not reminder.icon:
            reminder.icon = "💊" if reminder.category == "medication" else "🏃"
        reminders.append(reminder)
        self.save(reminders)
        return reminders

    def delete_at(self, index: int) -> List[Reminder]:
        reminders = self.load()
        if index < 0 or index >= len(reminders):
            raise IndexError("Invalid index")
        reminders.pop(index)
        self.save(reminders)
        return reminders

    def toggle_at(self, index: int) -> List[Reminder]:
        reminders = self.load()
        if index < 0 or index >= len(reminders):
            raise IndexError("Invalid index")
        reminders[index].enabled = not reminders[index].enabled
        self.save(reminders)
        return reminders


class ReminderService:
    def __init__(self, store: ReminderStore):
        self.store = store

    def due_reminders(self, now: Optional[datetime] = None) -> List[Reminder]:
        now = now or datetime.now()
        reminders = self.store.load()
        return [r for r in reminders if r.is_due(now)]

    def mark_alerted(self, reminder: Reminder, now: Optional[datetime] = None) -> None:
        now = now or datetime.now()
        reminders = self.store.load()
        for r in reminders:
            if (
                r.category == reminder.category
                and r.name == reminder.name
                and r.time_hhmm == reminder.time_hhmm
                and r.frequency == reminder.frequency
            ):
                r.mark_alerted(now)
        self.store.save(reminders)

    def filter_by(self, kind: Literal["medication", "activity", "all"]) -> List[Reminder]:
        reminders = self.store.load()
        if kind == "all":
            return reminders
        return [r for r in reminders if r.category == kind]

    def tick(self, notify: Callable[[Reminder], None], now: Optional[datetime] = None) -> int:
        now = now or datetime.now()
        due = self.due_reminders(now)
        if not due:
            return 0
        for r in due:
            notify(r)
            self.mark_alerted(r, now)
        return len(due)