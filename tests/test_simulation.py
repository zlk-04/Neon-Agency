from neon_agency.simulation import create_default_street, simulate_player_assault
import subprocess
import sys


def test_assault_creates_contextual_reactions_and_reputation_changes():
    simulation = create_default_street()

    result = simulate_player_assault(simulation, target_id="mira")

    assert result.event.kind == "assault"
    assert result.event.actor_id == "player"
    assert result.event.target_id == "mira"
    assert result.reactions_by_entity["mira"].actions == ("flee", "call_police")
    assert result.reactions_by_entity["rook"].actions == ("record_video",)
    assert result.reactions_by_entity["officer_chen"].actions == ("investigate",)
    assert simulation.city_reputation.player_violence_score == 10
    assert simulation.city_reputation.police_attention == 7


def test_npcs_remember_perceived_assaults():
    simulation = create_default_street()

    simulate_player_assault(simulation, target_id="mira")

    mira = simulation.entities["mira"]
    rook = simulation.entities["rook"]
    officer = simulation.entities["officer_chen"]

    assert [memory.event_kind for memory in mira.memories] == ["assault"]
    assert mira.memories[0].perception == "victim"
    assert rook.memories[0].perception == "witnessed"
    assert officer.memories[0].perception == "heard"


def test_rules_prevent_civilians_from_investigating_as_police():
    simulation = create_default_street()

    result = simulate_player_assault(simulation, target_id="rook")

    assert "investigate" not in result.reactions_by_entity["mira"].actions


def test_cli_demo_runs_from_installed_package():
    result = subprocess.run(
        [sys.executable, "-m", "neon_agency.main"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Action: attack Mira" in result.stdout
    assert "Officer Chen chooses: investigate" in result.stdout
