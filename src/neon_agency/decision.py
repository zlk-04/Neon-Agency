from neon_agency.models import Reaction
from neon_agency.rules import filter_allowed


def decide_reaction(entity, event, perception):
    if event.kind in {"assault", "threaten"} and perception in {"victim", "target"}:
        actions = _threatened_target_actions(entity)
        reason = "self-preservation after direct threat"
    elif event.kind == "steal" and perception == "target":
        actions = _theft_target_actions(entity)
        reason = "property crime response"
    elif event.kind == "help" and perception == "target":
        actions = ("thank",)
        reason = "positive response to help"
    elif event.kind == "talk" and perception == "target":
        actions = ("acknowledge",)
        reason = "social response"
    elif entity.is_police:
        actions = ("investigate",)
        reason = "police response to nearby incident"
    elif perception == "witnessed":
        actions = _witness_actions(entity, event)
        reason = "civilian witness response"
    else:
        actions = ("ignore",)
        reason = "no meaningful perception"

    return Reaction(
        entity_id=entity.entity_id,
        actions=filter_allowed(entity, actions),
        reason=reason,
    )


def _threatened_target_actions(entity):
    traits = entity.personality
    if traits.aggression >= 0.75 and traits.bravery >= 0.65:
        return ("fight_back",)
    if traits.lawfulness >= 0.5:
        return ("flee", "call_police")
    return ("flee",)


def _theft_target_actions(entity):
    if entity.personality.lawfulness >= 0.3:
        return ("call_police",)
    return ("confront",)


def _witness_actions(entity, event):
    traits = entity.personality
    if event.kind == "help":
        return ("approve",)
    if event.kind == "talk":
        return ("ignore",)
    if event.kind == "steal" and traits.lawfulness >= 0.3:
        return ("call_police",)
    if traits.aggression >= 0.8 and traits.bravery >= 0.7:
        return ("fight_back",)
    if traits.lawfulness >= 0.7:
        return ("call_police",)
    return ("record_video",)
