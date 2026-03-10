class DatabaseManager:
    def __init__(self):
        self.daily_records = {}

    def save_daily_status(self, elderly_id, health_status, medication_status, date):
        if elderly_id not in self.daily_records:
            self.daily_records[elderly_id] = []

        record = {
            "date": date,
            "health_status": health_status,
            "medication_status": medication_status
        }

        self.daily_records[elderly_id].append(record)
        return record

    def get_latest_daily_status(self, elderly_id):
        if elderly_id not in self.daily_records:
            return None
        if not self.daily_records[elderly_id]:
            return None
        return self.daily_records[elderly_id][-1]


class ElderlyUser:
    def __init__(self, elderly_id, database_manager):
        self.elderly_id = elderly_id
        self.database_manager = database_manager

    def submit_daily_status(self, health_status, medication_status, date):
        return self.database_manager.save_daily_status(
            self.elderly_id,
            health_status,
            medication_status,
            date
        )


class Carer:
    def __init__(self, carer_id, linked_elderly_id, system):
        self.carer_id = carer_id
        self.linked_elderly_id = linked_elderly_id
        self.system = system

    def open_dashboard(self):
        return self.system.view_daily_health_medication_status(self.linked_elderly_id)


class System:
    def __init__(self, database_manager):
        self.database_manager = database_manager

    def view_daily_health_medication_status(self, elderly_id):
        latest_status = self.database_manager.get_latest_daily_status(elderly_id)

        if latest_status is None:
            return {
                "success": False,
                "message": "No daily health and medication information found"
            }

        return {
            "success": True,
            "daily_status_summary": {
                "date": latest_status["date"],
                "health_status": latest_status["health_status"],
                "medication_status": latest_status["medication_status"]
            }
        }