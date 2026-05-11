from neon_agency.cli import handle_command
from neon_agency.simulation import create_default_street


def test_help_lists_available_commands():
    simulation = create_default_street()

    output = handle_command(simulation, "help")

    assert "attack <entity_id>" in output
    assert "steal <entity_id>" in output
    assert "threaten <entity_id>" in output
    assert "talk <entity_id>" in output
    assert "memories <entity_id>" in output
    assert "relationship <entity_id>" in output
    assert "relationships" in output
    assert "quit" in output


def test_status_shows_reputation_and_entities():
    simulation = create_default_street()

    output = handle_command(simulation, "status")

    assert "player_violence_score: 0" in output
    assert "police_attention: 0" in output
    assert "player_kindness_score: 0" in output
    assert "player_theft_score: 0" in output
    assert "civilian_trust: 0" in output
    assert "mira: Mira (civilian)" in output
    assert "officer_chen: Officer Chen (police)" in output


def test_attack_command_updates_world_and_formats_reactions():
    simulation = create_default_street()

    output = handle_command(simulation, "attack mira")

    assert "Action: attack Mira" in output
    assert "Mira chooses: flee + call_police" in output
    assert "Rook chooses: record_video" in output
    assert "Officer Chen chooses: investigate" in output
    assert simulation.city_reputation.player_violence_score == 10


def test_memories_command_shows_entity_memories():
    simulation = create_default_street()
    handle_command(simulation, "attack mira")

    output = handle_command(simulation, "memories mira")

    assert "Memories for Mira:" in output
    assert "victim assault by player against mira" in output


def test_unknown_command_returns_helpful_error():
    simulation = create_default_street()

    output = handle_command(simulation, "dance")

    assert "Unknown command: dance" in output
    assert "Type 'help'" in output


def test_invalid_attack_target_is_reported():
    simulation = create_default_street()

    output = handle_command(simulation, "attack nobody")

    assert "Unknown entity: nobody" in output


def test_help_command_updates_kindness_reputation():
    simulation = create_default_street()

    output = handle_command(simulation, "help mira")

    assert "Action: help Mira" in output
    assert "Mira chooses: thank" in output
    assert simulation.city_reputation.player_kindness_score == 6


def test_steal_command_updates_theft_reputation():
    simulation = create_default_street()

    output = handle_command(simulation, "steal rook")

    assert "Action: steal Rook" in output
    assert "Rook chooses: confront" in output
    assert simulation.city_reputation.player_theft_score == 8


def test_threaten_command_updates_violence_reputation():
    simulation = create_default_street()

    output = handle_command(simulation, "threaten mira")

    assert "Action: threaten Mira" in output
    assert "Mira chooses: flee + call_police" in output
    assert simulation.city_reputation.player_violence_score == 4


def test_talk_command_creates_social_memory():
    simulation = create_default_street()

    output = handle_command(simulation, "talk mira")

    assert "Action: talk Mira" in output
    assert "Mira chooses: acknowledge" in output
    assert simulation.entities["mira"].memories[0].event_kind == "talk"


def test_relationship_command_shows_single_npc_relationship():
    simulation = create_default_street()
    handle_command(simulation, "help mira")

    output = handle_command(simulation, "relationship mira")

    assert "Relationship for Mira:" in output
    assert "trust: 8" in output
    assert "fear: 0" in output
    assert "resentment: 0" in output
    assert "familiarity: 2" in output


def test_relationships_command_shows_all_npc_relationships():
    simulation = create_default_street()
    handle_command(simulation, "threaten mira")

    output = handle_command(simulation, "relationships")

    assert "Relationships:" in output
    assert "mira: trust=0 fear=7 resentment=4 familiarity=2" in output
    assert "rook: trust=0 fear=2 resentment=0 familiarity=1" in output
