from neon_agency.dialogue import generate_dialogue
from neon_agency.events import PlayerActionEvent
from neon_agency.models import Entity, Personality, Reaction


def make_entity():
    return Entity(
        entity_id="mira",
        name="Mira",
        role="civilian",
        location="street_03",
        personality=Personality(bravery=0.25, aggression=0.15, lawfulness=0.85),
    )


def make_event(kind):
    return PlayerActionEvent(
        kind=kind,
        actor_id="player",
        target_id="mira",
        location="street_03",
        severity=1,
        direct_witness_ids=(),
    )


def test_thank_dialogue_acknowledges_help():
    entity = make_entity()
    reaction = Reaction(entity_id="mira", actions=("thank",), reason="positive response to help")

    dialogue = generate_dialogue(entity, make_event("help"), reaction)

    assert dialogue == "Thanks. I will remember that you helped me."


def test_question_dialogue_mentions_prior_trust():
    entity = make_entity()
    entity.relationship_to_player.trust = 8
    reaction = Reaction(entity_id="mira", actions=("question",), reason="self-preservation after direct threat")

    dialogue = generate_dialogue(entity, make_event("threaten"), reaction)

    assert dialogue == "You helped me before. Why are you threatening me now?"


def test_confront_dialogue_uses_resentment():
    entity = make_entity()
    entity.relationship_to_player.resentment = 8
    reaction = Reaction(entity_id="mira", actions=("confront",), reason="property crime response")

    dialogue = generate_dialogue(entity, make_event("steal"), reaction)

    assert dialogue == "I am done letting this slide. Give it back."
