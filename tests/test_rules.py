from neon_agency.models import Entity, Personality
from neon_agency.rules import filter_allowed


def test_agent_intent_actions_are_world_allowed_for_civilians():
    entity = Entity(
        entity_id="mira",
        name="Mira",
        role="civilian",
        location="street_03",
        personality=Personality(bravery=0.25, aggression=0.15, lawfulness=0.85),
    )

    actions = filter_allowed(
        entity,
        (
            "warn_player",
            "question_player",
            "comfort_target",
            "confront_player",
            "report_to_police",
        ),
    )

    assert actions == (
        "warn_player",
        "question_player",
        "comfort_target",
        "confront_player",
        "report_to_police",
    )
