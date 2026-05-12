from neon_agency.simulation import simulate_player_action


ACTION_ALIASES = {
    "attack": "assault",
    "help": "help",
    "steal": "steal",
    "threaten": "threaten",
    "talk": "talk",
}


def serialize_state(simulation, last_result=None):
    state = {
        "city_reputation": _serialize_reputation(simulation.city_reputation),
        "entities": {
            entity_id: _serialize_entity(entity)
            for entity_id, entity in simulation.entities.items()
        },
    }
    if last_result is not None:
        state["last_result"] = last_result
    return state


def handle_state_request(simulation, last_result=None):
    return {"status": 200, "body": serialize_state(simulation, last_result=last_result)}


def handle_action_request(simulation, payload, dialogue_provider=None):
    action = payload.get("action") if isinstance(payload, dict) else None
    target = payload.get("target") if isinstance(payload, dict) else None

    if action not in ACTION_ALIASES:
        return _error(
            400,
            "invalid_action",
            f"Unsupported action: {action}",
            allowed_actions=list(ACTION_ALIASES.keys()),
        )
    if target not in simulation.entities or target == "player":
        return _error(400, "invalid_target", f"Unknown target: {target}")

    result = simulate_player_action(
        simulation,
        action_kind=ACTION_ALIASES[action],
        target_id=target,
        dialogue_provider=dialogue_provider,
    )
    body = serialize_result(result)
    body["state"] = serialize_state(simulation, last_result=serialize_result(result))
    return {"status": 200, "body": body}


def handle_reset_request(create_simulation):
    simulation = create_simulation()
    return {
        "status": 200,
        "body": {
            "state": serialize_state(simulation),
        },
        "simulation": simulation,
    }


def serialize_result(result):
    return {
        "event": _serialize_event(result.event),
        "reactions": {
            entity_id: _serialize_reaction(reaction)
            for entity_id, reaction in result.reactions_by_entity.items()
        },
    }


def _serialize_reputation(reputation):
    return {
        "player_violence_score": reputation.player_violence_score,
        "player_kindness_score": reputation.player_kindness_score,
        "player_theft_score": reputation.player_theft_score,
        "police_attention": reputation.police_attention,
        "civilian_trust": reputation.civilian_trust,
    }


def _serialize_entity(entity):
    return {
        "id": entity.entity_id,
        "name": entity.name,
        "role": entity.role,
        "location": entity.location,
        "relationship": _serialize_relationship(entity.relationship_to_player),
        "memories": [_serialize_memory(memory) for memory in entity.memories],
    }


def _serialize_relationship(relationship):
    return {
        "trust": relationship.trust,
        "fear": relationship.fear,
        "resentment": relationship.resentment,
        "familiarity": relationship.familiarity,
    }


def _serialize_memory(memory):
    return {
        "event_kind": memory.event_kind,
        "actor_id": memory.actor_id,
        "target_id": memory.target_id,
        "perception": memory.perception,
        "summary": memory.summary,
    }


def _serialize_event(event):
    return {
        "kind": event.kind,
        "actor_id": event.actor_id,
        "target_id": event.target_id,
        "location": event.location,
        "severity": event.severity,
        "direct_witness_ids": list(event.direct_witness_ids),
    }


def _serialize_reaction(reaction):
    return {
        "entity_id": reaction.entity_id,
        "actions": list(reaction.actions),
        "reason": reaction.reason,
        "dialogue": reaction.dialogue,
        "dialogue_source": reaction.dialogue_source,
        "dialogue_error": reaction.dialogue_error,
    }


def _error(status, error, message, **extra):
    body = {
        "error": error,
        "message": message,
    }
    body.update(extra)
    return {"status": status, "body": body}
