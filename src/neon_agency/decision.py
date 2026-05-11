from neon_agency.models import Reaction
from neon_agency.rules import filter_allowed


def decide_reaction(entity, event, perception):
    if perception == "victim":
        actions = _victim_actions(entity)
        reason = "self-preservation after direct assault"
    elif entity.is_police:
        actions = ("investigate",)
        reason = "police response to nearby violence"
    elif perception == "witnessed":
        actions = _witness_actions(entity)
        reason = "civilian witness response"
    else:
        actions = ("ignore",)
        reason = "no meaningful perception"

    return Reaction(
        entity_id=entity.entity_id,
        actions=filter_allowed(entity, actions),
        reason=reason,
    )


def _victim_actions(entity):
    traits = entity.personality
    if traits.aggression >= 0.75 and traits.bravery >= 0.65:
        return ("fight_back",)
    if traits.lawfulness >= 0.5:
        return ("flee", "call_police")
    return ("flee",)


def _witness_actions(entity):
    traits = entity.personality
    if traits.aggression >= 0.8 and traits.bravery >= 0.7:
        return ("fight_back",)
    if traits.lawfulness >= 0.7:
        return ("call_police",)
    return ("record_video",)
