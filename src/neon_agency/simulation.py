from neon_agency.decision import decide_reaction
from neon_agency.dialogue import generate_dialogue_result
from neon_agency.events import AssaultEvent, PlayerActionEvent
from neon_agency.models import CityReputation, Entity, Personality, Reaction, Simulation, SimulationResult
from neon_agency.perception import perceive_event


ACTION_SEVERITY = {
    "assault": 10,
    "help": 2,
    "steal": 8,
    "threaten": 4,
    "talk": 1,
}

RELATIONSHIP_DELTAS = {
    ("help", "target"): {"trust": 8, "familiarity": 2},
    ("help", "witnessed"): {"trust": 2, "familiarity": 1},
    ("assault", "victim"): {"fear": 8, "resentment": 6, "familiarity": 2},
    ("assault", "witnessed"): {"fear": 3, "resentment": 1, "familiarity": 1},
    ("steal", "target"): {"fear": 2, "resentment": 8, "familiarity": 2},
    ("steal", "witnessed"): {"resentment": 2, "familiarity": 1},
    ("threaten", "target"): {"fear": 7, "resentment": 4, "familiarity": 2},
    ("threaten", "witnessed"): {"fear": 2, "familiarity": 1},
    ("talk", "target"): {"trust": 1, "familiarity": 3},
    ("talk", "witnessed"): {"familiarity": 1},
}


def create_default_street():
    return Simulation(
        entities={
            "player": Entity(
                entity_id="player",
                name="Player",
                role="player",
                location="street_03",
                personality=Personality(bravery=1.0, aggression=0.0, lawfulness=0.0),
            ),
            "mira": Entity(
                entity_id="mira",
                name="Mira",
                role="civilian",
                location="street_03",
                personality=Personality(bravery=0.25, aggression=0.15, lawfulness=0.85),
            ),
            "rook": Entity(
                entity_id="rook",
                name="Rook",
                role="civilian",
                location="street_03",
                personality=Personality(bravery=0.72, aggression=0.62, lawfulness=0.35),
            ),
            "officer_chen": Entity(
                entity_id="officer_chen",
                name="Officer Chen",
                role="police",
                location="street_03",
                personality=Personality(bravery=0.9, aggression=0.45, lawfulness=1.0),
            ),
        },
        city_reputation=CityReputation(),
    )


def simulate_player_assault(simulation, target_id):
    return simulate_player_action(simulation, action_kind="assault", target_id=target_id)


def simulate_player_action(simulation, action_kind, target_id, dialogue_provider=None):
    if action_kind not in ACTION_SEVERITY:
        raise ValueError(f"Unsupported action kind: {action_kind}")

    target = simulation.entities[target_id]
    witness_ids = tuple(
        entity_id
        for entity_id, entity in simulation.entities.items()
        if entity_id not in {"player", target_id}
        and entity.location == target.location
        and not entity.is_police
    )
    event_class = AssaultEvent if action_kind == "assault" else PlayerActionEvent
    event_kwargs = {
        "actor_id": "player",
        "target_id": target_id,
        "location": target.location,
        "severity": ACTION_SEVERITY[action_kind],
        "direct_witness_ids": witness_ids,
    }
    if action_kind != "assault":
        event_kwargs["kind"] = action_kind
    event = event_class(**event_kwargs)

    perceptions = perceive_event(simulation, event)
    _apply_relationships(simulation, event, perceptions)
    reactions = {
        entity_id: decide_reaction(simulation.entities[entity_id], event, perception)
        for entity_id, perception in perceptions.items()
    }
    reactions = _attach_dialogue(simulation, event, reactions, dialogue_provider)
    _apply_reputation(simulation, event, reactions)

    return SimulationResult(event=event, reactions_by_entity=reactions)


def _apply_relationships(simulation, event, perceptions):
    for entity_id, perception in perceptions.items():
        entity = simulation.entities[entity_id]
        delta = RELATIONSHIP_DELTAS.get((event.kind, perception), {})
        entity.relationship_to_player.apply(**delta)


def _attach_dialogue(simulation, event, reactions, dialogue_provider=None):
    reactions_with_dialogue = {}
    for entity_id, reaction in reactions.items():
        dialogue = generate_dialogue_result(
            simulation.entities[entity_id],
            event,
            reaction,
            provider=dialogue_provider,
        )
        reactions_with_dialogue[entity_id] = _with_dialogue(reaction, dialogue)
    return reactions_with_dialogue


def _with_dialogue(reaction, dialogue):
    return Reaction(
        entity_id=reaction.entity_id,
        actions=reaction.actions,
        reason=reaction.reason,
        dialogue=dialogue.text,
        dialogue_source=dialogue.source,
        dialogue_error=dialogue.error,
    )


def _apply_reputation(simulation, event, reactions):
    if event.kind == "assault":
        simulation.city_reputation.player_violence_score += 10
    elif event.kind == "help":
        simulation.city_reputation.player_kindness_score += 6
        simulation.city_reputation.civilian_trust += 4
    elif event.kind == "steal":
        simulation.city_reputation.player_theft_score += 8
        simulation.city_reputation.civilian_trust -= 3
    elif event.kind == "threaten":
        simulation.city_reputation.player_violence_score += 4
        simulation.city_reputation.civilian_trust -= 2
    elif event.kind == "talk":
        simulation.city_reputation.civilian_trust += 1

    if any("call_police" in reaction.actions for reaction in reactions.values()):
        simulation.city_reputation.police_attention += 5
    if any("investigate" in reaction.actions for reaction in reactions.values()):
        simulation.city_reputation.police_attention += 2
