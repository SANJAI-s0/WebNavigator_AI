# webnavigator_ai/utils/schema.py
from dataclasses import dataclass, asdict
from typing import Optional, Any, Dict
from datetime import datetime


@dataclass
class NormalizedSearchResult:
    title: str
    snippet: str
    url: str
    source: str
    published_at: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None

    def to_dict(self):
        return asdict(self)


def timestamp_iso():
    return datetime.utcnow().isoformat() + "Z"
