import json

from neon_agency.decision import decide_reaction
from neon_agency.models import Reaction


ALLOWED_AGENT_ACTIONS = (
    "ignore",
    "thank",
    "approve",
    "warn_player",
    "question_player",
    "comfort_target",
    "call_police",
    "confront_player",
    "flee",
    "report_to_police",
)


def build_decision_prompt(entity, event, perception):
    relationship = entity.relationship_to_player
    allowed_actions = ", ".join(ALLOWED_AGENT_ACTIONS)
    memory_lines = "\n".join(f"- {memory.summary}" for memory in entity.memories[-3:]) or "- None"
    return "\n".join(
        [
            "Choose one NPC behavior intent for this game simulation.",
            "Use only the provided world state and allowed actions.",
            "Do not explain your reasoning.",
            f"NPC: {entity.name}",
            f"Role: {entity.role}",
            f"Perception: {perception}",
            f"Event: {event.kind} by {event.actor_id} targeting {event.target_id}",
            (
                "Relationship to player: "
                f"trust={relationship.trust} "
                f"fear={relationship.fear} "
                f"resentment={relationship.resentment} "
                f"familiarity={relationship.familiarity}"
            ),
            "Recent memories:",
            memory_lines,
            f"Allowed actions: {allowed_actions}",
            (
                "Return only JSON with keys: "
                "action, target_id, reason, dialogue."
            ),
        ]
    )


def decide_agent_reaction(entity, event, perception, provider=None, fallback_decider=decide_reaction):
    fallback = fallback_decider(entity, event, perception)
    if provider is None:
        return fallback

    prompt = build_decision_prompt(entity, event, perception)
    try:
        raw_response = provider.generate(prompt).strip()
    except Exception as exc:
        return _with_policy_error(fallback, str(exc) or exc.__class__.__name__)

    try:
        intent = json.loads(raw_response)
    except json.JSONDecodeError:
        return _with_policy_error(fallback, "decision provider returned invalid JSON")

    action = intent.get("action") if isinstance(intent, dict) else None
    if action not in ALLOWED_AGENT_ACTIONS:
        return _with_policy_error(
            fallback,
            f"decision provider returned unsupported action: {action}",
        )

    reason = _clean_text(intent.get("reason")) or fallback.reason
    dialogue = _clean_text(intent.get("dialogue"))
    return Reaction(
        entity_id=entity.entity_id,
        actions=(action,),
        reason=reason,
        dialogue=dialogue,
        dialogue_source="deepseek" if dialogue else "template",
        dialogue_error="",
    )


def _with_policy_error(reaction, error):
    return Reaction(
        entity_id=reaction.entity_id,
        actions=reaction.actions,
        reason=reaction.reason,
        dialogue=reaction.dialogue,
        dialogue_source=reaction.dialogue_source,
        dialogue_error=error,
    )


def _clean_text(value):
    if not isinstance(value, str):
        return ""
    return value.strip()
