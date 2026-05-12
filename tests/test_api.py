import json

from neon_agency.api import handle_action_request, serialize_state
from neon_agency.server import NeonAgencyServer
from neon_agency.simulation import create_default_street


def test_serialize_state_includes_reputation_entities_relationships_and_memories():
    simulation = create_default_street()

    state = serialize_state(simulation)

    assert state["city_reputation"] == {
        "player_violence_score": 0,
        "player_kindness_score": 0,
        "player_theft_score": 0,
        "police_attention": 0,
        "civilian_trust": 0,
    }
    assert state["entities"]["mira"] == {
        "id": "mira",
        "name": "Mira",
        "role": "civilian",
        "location": "street_03",
        "relationship": {
            "trust": 0,
            "fear": 0,
            "resentment": 0,
            "familiarity": 0,
        },
        "memories": [],
    }
    assert "player" in state["entities"]


def test_handle_action_request_runs_action_and_returns_result_with_updated_state():
    simulation = create_default_street()

    response = handle_action_request(simulation, {"action": "help", "target": "mira"})

    assert response["status"] == 200
    body = response["body"]
    assert body["event"] == {
        "kind": "help",
        "actor_id": "player",
        "target_id": "mira",
        "location": "street_03",
        "severity": 2,
        "direct_witness_ids": ["rook"],
    }
    assert body["reactions"]["mira"]["actions"] == ["thank"]
    assert body["reactions"]["mira"]["dialogue_source"] == "template"
    assert body["state"]["city_reputation"]["player_kindness_score"] == 6
    assert body["state"]["entities"]["mira"]["relationship"]["trust"] == 8
    assert body["state"]["last_result"]["event"]["kind"] == "help"
    json.dumps(body)


def test_handle_action_request_rejects_unknown_action_without_mutating_state():
    simulation = create_default_street()

    response = handle_action_request(simulation, {"action": "dance", "target": "mira"})

    assert response == {
        "status": 400,
        "body": {
            "error": "invalid_action",
            "message": "Unsupported action: dance",
            "allowed_actions": ["attack", "help", "steal", "threaten", "talk"],
        },
    }
    assert simulation.city_reputation.player_kindness_score == 0
    assert simulation.entities["mira"].memories == []


def test_handle_action_request_rejects_unknown_target_without_mutating_state():
    simulation = create_default_street()

    response = handle_action_request(simulation, {"action": "help", "target": "nobody"})

    assert response == {
        "status": 400,
        "body": {
            "error": "invalid_target",
            "message": "Unknown target: nobody",
        },
    }
    assert simulation.city_reputation.player_kindness_score == 0
    assert simulation.entities["mira"].memories == []


def test_server_keeps_last_result_available_after_action():
    server = NeonAgencyServer()

    server.action({"action": "help", "target": "mira"})
    response = server.state()

    assert response["status"] == 200
    assert response["body"]["last_result"]["event"]["kind"] == "help"
