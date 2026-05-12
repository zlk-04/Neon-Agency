from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class DialogueResult:
    text: str
    source: str
    error: str = ""


@dataclass(frozen=True)
class DialogueContext:
    npc_name: str
    npc_role: str
    event_kind: str
    actor_id: str
    target_id: str
    actions: Tuple[str, ...]
    reason: str
    trust: int
    fear: int
    resentment: int
    familiarity: int
    recent_memories: Tuple[str, ...]


def build_dialogue_context(entity, event, reaction):
    relationship = entity.relationship_to_player
    recent_memories = tuple(memory.summary for memory in entity.memories[-3:])
    return DialogueContext(
        npc_name=entity.name,
        npc_role=entity.role,
        event_kind=event.kind,
        actor_id=event.actor_id,
        target_id=event.target_id,
        actions=reaction.actions,
        reason=reaction.reason,
        trust=relationship.trust,
        fear=relationship.fear,
        resentment=relationship.resentment,
        familiarity=relationship.familiarity,
        recent_memories=recent_memories,
    )


def build_dialogue_prompt(context):
    memory_lines = "\n".join(f"- {memory}" for memory in context.recent_memories) or "- None"
    actions = " + ".join(context.actions)
    return "\n".join(
        [
            "Write one short in-character NPC line for a game simulation.",
            "Use only the provided state. Do not invent new actions or facts.",
            "Do not explain your reasoning, task, or interpretation.",
            f"NPC: {context.npc_name}",
            f"Role: {context.npc_role}",
            f"Event: {context.event_kind} by {context.actor_id} targeting {context.target_id}",
            f"Reaction: {actions}",
            f"Reason: {context.reason}",
            (
                "Relationship: "
                f"trust={context.trust} "
                f"fear={context.fear} "
                f"resentment={context.resentment} "
                f"familiarity={context.familiarity}"
            ),
            "Recent memories:",
            memory_lines,
            "Return only the dialogue line, without speaker name or quotes.",
        ]
    )


def generate_dialogue(entity, event, reaction, provider=None):
    return generate_dialogue_result(entity, event, reaction, provider=provider).text


def generate_dialogue_result(entity, event, reaction, provider=None):
    if provider is not None:
        prompt = build_dialogue_prompt(build_dialogue_context(entity, event, reaction))
        try:
            generated = provider.generate(prompt).strip()
        except Exception as exc:
            generated = ""
            error = str(exc) or exc.__class__.__name__
        else:
            error = ""
        if generated:
            if _looks_like_reasoning_analysis(generated):
                return DialogueResult(
                    text=generate_template_dialogue(entity, event, reaction),
                    source="template",
                    error="provider returned reasoning analysis instead of dialogue",
                )
            return DialogueResult(text=generated, source="deepseek")
        if not error:
            error = "provider returned blank dialogue"

        return DialogueResult(
            text=generate_template_dialogue(entity, event, reaction),
            source="template",
            error=error,
        )

    return DialogueResult(text=generate_template_dialogue(entity, event, reaction), source="template")


def generate_template_dialogue(entity, event, reaction):
    actions = reaction.actions
    relationship = entity.relationship_to_player

    if "thank" in actions:
        return "Thanks. I will remember that you helped me."
    if "question" in actions:
        if relationship.trust >= 8:
            return "You helped me before. Why are you threatening me now?"
        return "Why are you doing this?"
    if "flee" in actions:
        return "Stay away from me."
    if "call_police" in actions:
        return "I am calling the police."
    if "confront" in actions:
        if event.kind == "steal":
            return "I am done letting this slide. Give it back."
        return "I am not ignoring this anymore."
    if "warmly_greet" in actions:
        return "It is good to see you."
    if "acknowledge" in actions:
        return "Hey."
    if "record_video" in actions:
        return "I am recording this."
    if "investigate" in actions:
        return "I need to know what happened here."
    if "approve" in actions:
        return "That was decent of you."
    return ""


def _looks_like_reasoning_analysis(text):
    lowered = text.lower()
    analysis_markers = (
        "we need to generate",
        "need to generate",
        "single line of dialogue",
        "the npc",
        "reacting to the player",
    )
    return sum(marker in lowered for marker in analysis_markers) >= 2
