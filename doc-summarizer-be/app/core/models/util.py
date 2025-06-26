from datetime import datetime, timezone


def datetime_now_sec() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)
