import json
from pathlib import Path
from typing import Dict, Optional


class AgentMemory:
    def __init__(self, path: str = ".agent_memory.json"):
        self.path = Path(path)
        self._data: Dict = self._load()

    def _load(self) -> Dict:
        if self.path.exists():
            return json.loads(self.path.read_text())
        return {"queries": {}, "domains": {}}

    def save(self):
        self.path.write_text(json.dumps(self._data, indent=2))

    # --------------------------------------------------
    # Query memory
    # --------------------------------------------------
    def remember_query(self, query: str, url: str):
        self._data["queries"][query.lower()] = url
        self.save()

    def recall_query(self, query: str) -> Optional[str]:
        return self._data["queries"].get(query.lower())

    # --------------------------------------------------
    # Domain memory
    # --------------------------------------------------
    def reinforce_domain(self, url: str):
        domain = url.split("/")[2]
        self._data["domains"].setdefault(domain, 0)
        self._data["domains"][domain] += 1
        self.save()

    def trusted_domains(self):
        return sorted(
            self._data["domains"],
            key=self._data["domains"].get,
            reverse=True,
        )
