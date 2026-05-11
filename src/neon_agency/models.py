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
class Relationship:
    trust: int = 0
    fear: int = 0
    resentment: int = 0
    familiarity: int = 0

    def apply(self, trust=0, fear=0, resentment=0, familiarity=0):
        self.trust += trust
        self.fear += fear
        self.resentment += resentment
        self.familiarity += familiarity


@dataclass
class Entity:
    entity_id: str
    name: str
    role: str
    location: str
    personality: Personality
    relationship_to_player: Relationship = field(default_factory=Relationship)
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
    dialogue: str = ""
    dialogue_source: str = "template"
    dialogue_error: str = ""


@dataclass
class Simulation:
    entities: Dict[str, Entity]
    city_reputation: CityReputation = field(default_factory=CityReputation)


@dataclass(frozen=True)
class SimulationResult:
    event: object
    reactions_by_entity: Dict[str, Reaction]
