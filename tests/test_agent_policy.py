from neon_agency.agent_policy import build_decision_prompt, decide_agent_reaction
from neon_agency.events import PlayerActionEvent
from neon_agency.models import Entity, Personality, Reaction


class Provider:
    def __init__(self, response):
        self.response = response
        self.prompts = []

    def generate(self, prompt):
        self.prompts.append(prompt)
        return self.response


class FailingProvider:
    def generate(self, prompt):
        raise RuntimeError("model unavailable")


def make_entity():
    entity = Entity(
        entity_id="mira",
        name="Mira",
        role="civilian",
        location="street_03",
        personality=Personality(bravery=0.25, aggression=0.15, lawfulness=0.85),
    )
    entity.relationship_to_player.trust = 18
    entity.relationship_to_player.familiarity = 5
    return entity


def make_event():
    return PlayerActionEvent(
        kind="help",
        actor_id="player",
        target_id="officer_chen",
        location="street_03",
        severity=2,
        direct_witness_ids=("mira", "rook"),
    )


def fallback_decider(entity, event, perception):
    return Reaction(entity_id=entity.entity_id, actions=("approve",), reason="fallback rule")


def test_agent_policy_uses_valid_structured_intent():
    provider = Provider(
        '{"action":"warn_player","target_id":"player","reason":"Mira trusts the player but worries about police involvement.","dialogue":"You keep helping people. Just be careful around Chen."}'
    )

    reaction = decide_agent_reaction(make_entity(), make_event(), "witnessed", provider, fallback_decider)

    assert reaction.entity_id == "mira"
    assert reaction.actions == ("warn_player",)
    assert reaction.reason == "Mira trusts the player but worries about police involvement."
    assert reaction.dialogue == "You keep helping people. Just be careful around Chen."
    assert reaction.dialogue_source == "deepseek"
    assert reaction.dialogue_error == ""
    assert provider.prompts


def test_agent_policy_falls_back_for_unknown_action():
    provider = Provider('{"action":"teleport","target_id":"mira","reason":"Break physics.","dialogue":"Watch this."}')

    reaction = decide_agent_reaction(make_entity(), make_event(), "witnessed", provider, fallback_decider)

    assert reaction.actions == ("approve",)
    assert reaction.reason == "fallback rule"
    assert reaction.dialogue == ""
    assert reaction.dialogue_source == "template"
    assert reaction.dialogue_error == "decision provider returned unsupported action: teleport"


def test_agent_policy_falls_back_for_non_json_output():
    provider = Provider("Mira warns the player to be careful.")

    reaction = decide_agent_reaction(make_entity(), make_event(), "witnessed", provider, fallback_decider)

    assert reaction.actions == ("approve",)
    assert reaction.dialogue_error == "decision provider returned invalid JSON"


def test_agent_policy_falls_back_for_provider_exception():
    reaction = decide_agent_reaction(make_entity(), make_event(), "witnessed", FailingProvider(), fallback_decider)

    assert reaction.actions == ("approve",)
    assert reaction.dialogue_error == "model unavailable"


def test_decision_prompt_includes_world_rules_and_context():
    prompt = build_decision_prompt(make_entity(), make_event(), "witnessed")

    assert "NPC: Mira" in prompt
    assert "Perception: witnessed" in prompt
    assert "Event: help by player targeting officer_chen" in prompt
    assert "Allowed actions:" in prompt
    assert "warn_player" in prompt
    assert "Return only JSON" in prompt
