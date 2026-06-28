from datetime import datetime


def get_now() -> datetime:
    """現在日時を返す"""
    return datetime.now()


def get_today_str() -> str:
    """今日の日付をYYYY-MM-DD形式で返す"""
    return get_now().strftime("%Y-%m-%d")


def format_date_jp(date_str: str) -> str:
    """YYYY-MM-DD → 例: 2026年6月28日"""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return f"{dt.year}年{dt.month}月{dt.day}日"


def format_date_short(date_str: str) -> str:
    """YYYY-MM-DD → 例: 6月28日"""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return f"{dt.month}月{dt.day}日"


def format_date_dot(date_str: str) -> str:
    """YYYY-MM-DD → 例: 2026.06.28"""
    return date_str.replace("-", ".")
