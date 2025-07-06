from datetime import datetime

def filter_by_date_range(data, start_date=None, end_date=None):
    if start_date:
        start = datetime.fromisoformat(start_date)
        data = [entry for entry in data if datetime.fromisoformat(entry["timestamp"]) >= start]
    if end_date:
        end = datetime.fromisoformat(end_date)
        data = [entry for entry in data if datetime.fromisoformat(entry["timestamp"]) <= end]
    return data