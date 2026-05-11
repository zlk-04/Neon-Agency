from neon_agency.dialogue import build_dialogue_context, build_dialogue_prompt, generate_dialogue, generate_dialogue_result
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


def test_prompt_includes_event_relationship_reaction_and_memory():
    entity = make_entity()
    entity.relationship_to_player.trust = 8
    entity.memories.append(
        type(
            "MemoryStub",
            (),
            {
                "event_kind": "help",
                "actor_id": "player",
                "target_id": "mira",
                "perception": "target",
                "summary": "Mira target help by player against mira.",
            },
        )()
    )
    reaction = Reaction(entity_id="mira", actions=("question",), reason="self-preservation after direct threat")

    context = build_dialogue_context(entity, make_event("threaten"), reaction)
    prompt = build_dialogue_prompt(context)

    assert "NPC: Mira" in prompt
    assert "Event: threaten by player targeting mira" in prompt
    assert "Relationship: trust=8 fear=0 resentment=0 familiarity=0" in prompt
    assert "Reaction: question" in prompt
    assert "Recent memories:" in prompt
    assert "target help by player against mira" in prompt


class FakeProvider:
    def __init__(self, response):
        self.response = response
        self.prompts = []

    def generate(self, prompt):
        self.prompts.append(prompt)
        return self.response


class FailingProvider:
    def generate(self, prompt):
        raise RuntimeError("provider failed")


def test_generate_dialogue_uses_provider_response_when_available():
    entity = make_entity()
    reaction = Reaction(entity_id="mira", actions=("thank",), reason="positive response to help")
    provider = FakeProvider("I can say this in my own words.")

    dialogue = generate_dialogue(entity, make_event("help"), reaction, provider=provider)

    assert dialogue == "I can say this in my own words."
    assert provider.prompts


def test_generate_dialogue_result_marks_provider_source():
    entity = make_entity()
    reaction = Reaction(entity_id="mira", actions=("thank",), reason="positive response to help")

    result = generate_dialogue_result(entity, make_event("help"), reaction, provider=FakeProvider("Generated line."))

    assert result.text == "Generated line."
    assert result.source == "deepseek"
    assert result.error == ""


def test_generate_dialogue_falls_back_when_provider_returns_blank():
    entity = make_entity()
    reaction = Reaction(entity_id="mira", actions=("thank",), reason="positive response to help")

    dialogue = generate_dialogue(entity, make_event("help"), reaction, provider=FakeProvider("   "))

    assert dialogue == "Thanks. I will remember that you helped me."


def test_generate_dialogue_result_marks_blank_provider_fallback():
    entity = make_entity()
    reaction = Reaction(entity_id="mira", actions=("thank",), reason="positive response to help")

    result = generate_dialogue_result(entity, make_event("help"), reaction, provider=FakeProvider("   "))

    assert result.text == "Thanks. I will remember that you helped me."
    assert result.source == "template"
    assert result.error == "provider returned blank dialogue"


def test_generate_dialogue_falls_back_when_provider_fails():
    entity = make_entity()
    reaction = Reaction(entity_id="mira", actions=("thank",), reason="positive response to help")

    dialogue = generate_dialogue(entity, make_event("help"), reaction, provider=FailingProvider())

    assert dialogue == "Thanks. I will remember that you helped me."


def test_generate_dialogue_result_marks_provider_exception_fallback():
    entity = make_entity()
    reaction = Reaction(entity_id="mira", actions=("thank",), reason="positive response to help")

    result = generate_dialogue_result(entity, make_event("help"), reaction, provider=FailingProvider())

    assert result.text == "Thanks. I will remember that you helped me."
    assert result.source == "template"
    assert "provider failed" in result.error
