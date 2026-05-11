from neon_agency.decision import decide_reaction
from neon_agency.events import AssaultEvent
from neon_agency.models import CityReputation, Entity, Personality, Simulation, SimulationResult
from neon_agency.perception import perceive_assault


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
    target = simulation.entities[target_id]
    witness_ids = tuple(
        entity_id
        for entity_id, entity in simulation.entities.items()
        if entity_id not in {"player", target_id}
        and entity.location == target.location
        and not entity.is_police
    )
    event = AssaultEvent(
        actor_id="player",
        target_id=target_id,
        location=target.location,
        severity=10,
        direct_witness_ids=witness_ids,
    )

    perceptions = perceive_assault(simulation, event)
    reactions = {
        entity_id: decide_reaction(simulation.entities[entity_id], event, perception)
        for entity_id, perception in perceptions.items()
    }
    _apply_reputation(simulation, reactions)

    return SimulationResult(event=event, reactions_by_entity=reactions)


def _apply_reputation(simulation, reactions):
    simulation.city_reputation.player_violence_score += 10
    if any("call_police" in reaction.actions for reaction in reactions.values()):
        simulation.city_reputation.police_attention += 5
    if any("investigate" in reaction.actions for reaction in reactions.values()):
        simulation.city_reputation.police_attention += 2
