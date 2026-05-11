from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PlayerActionEvent:
    kind: str
    actor_id: str
    target_id: str
    location: str
    severity: int
    direct_witness_ids: Tuple[str, ...]


@dataclass(frozen=True)
class AssaultEvent:
    actor_id: str
    target_id: str
    location: str
    severity: int
    direct_witness_ids: Tuple[str, ...]

    kind: str = "assault"
