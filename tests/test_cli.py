from neon_agency.cli import handle_command
from neon_agency.simulation import create_default_street


def test_help_lists_available_commands():
    simulation = create_default_street()

    output = handle_command(simulation, "help")

    assert "attack <entity_id>" in output
    assert "memories <entity_id>" in output
    assert "quit" in output


def test_status_shows_reputation_and_entities():
    simulation = create_default_street()

    output = handle_command(simulation, "status")

    assert "player_violence_score: 0" in output
    assert "police_attention: 0" in output
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
