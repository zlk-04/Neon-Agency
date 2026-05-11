from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass(frozen=True)
class Personality:
    bravery: float
    aggression: float
    lawfulness: float


@dataclass
class Memory:
    event_kind: str
    actor_id: str
    target_id: str
    perception: str
    summary: str


@dataclass
class Entity:
    entity_id: str
    name: str
    role: str
    location: str
    personality: Personality
    relationship_to_player: float = 0.0
    memories: list = field(default_factory=list)

    @property
    def is_police(self) -> bool:
        return self.role == "police"


@dataclass
class CityReputation:
    player_violence_score: int = 0
    player_kindness_score: int = 0
    player_theft_score: int = 0
    police_attention: int = 0
    civilian_trust: int = 0


@dataclass(frozen=True)
class Reaction:
    entity_id: str
    actions: Tuple[str, ...]
    reason: str


@dataclass
class Simulation:
    entities: Dict[str, Entity]
    city_reputation: CityReputation = field(default_factory=CityReputation)


@dataclass(frozen=True)
class SimulationResult:
    event: object
    reactions_by_entity: Dict[str, Reaction]
