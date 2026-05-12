from neon_agency.simulation import create_default_street, simulate_player_action, simulate_player_assault
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
        [sys.executable, "-m", "neon_agency.main", "--demo"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Action: attack Mira" in result.stdout
    assert "Officer Chen chooses: investigate" in result.stdout


def test_default_entrypoint_runs_interactive_shell_commands():
    result = subprocess.run(
        [sys.executable, "-m", "neon_agency.main"],
        input="status\nquit\n",
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Neon Agency interactive sandbox" in result.stdout
    assert "player_violence_score: 0" in result.stdout
    assert "Goodbye." in result.stdout


def test_help_action_builds_trust_and_kindness_memory():
    simulation = create_default_street()

    result = simulate_player_action(simulation, action_kind="help", target_id="mira")

    assert result.event.kind == "help"
    assert result.reactions_by_entity["mira"].actions == ("thank",)
    assert result.reactions_by_entity["rook"].actions == ("approve",)
    assert simulation.city_reputation.player_kindness_score == 6
    assert simulation.city_reputation.civilian_trust == 4
    assert simulation.entities["mira"].memories[0].event_kind == "help"


def test_steal_action_increases_theft_and_police_attention():
    simulation = create_default_street()

    result = simulate_player_action(simulation, action_kind="steal", target_id="rook")

    assert result.event.kind == "steal"
    assert result.reactions_by_entity["rook"].actions == ("confront",)
    assert result.reactions_by_entity["mira"].actions == ("call_police",)
    assert result.reactions_by_entity["officer_chen"].actions == ("investigate",)
    assert simulation.city_reputation.player_theft_score == 8
    assert simulation.city_reputation.police_attention == 7


def test_threaten_action_creates_intimidation_reactions():
    simulation = create_default_street()

    result = simulate_player_action(simulation, action_kind="threaten", target_id="mira")

    assert result.event.kind == "threaten"
    assert result.reactions_by_entity["mira"].actions == ("flee", "call_police")
    assert result.reactions_by_entity["rook"].actions == ("record_video",)
    assert simulation.city_reputation.player_violence_score == 4
    assert simulation.city_reputation.police_attention == 7


def test_talk_action_creates_social_memory_without_police_attention():
    simulation = create_default_street()

    result = simulate_player_action(simulation, action_kind="talk", target_id="mira")

    assert result.event.kind == "talk"
    assert result.reactions_by_entity["mira"].actions == ("acknowledge",)
    assert "officer_chen" not in result.reactions_by_entity
    assert simulation.city_reputation.civilian_trust == 1
    assert simulation.city_reputation.police_attention == 0


def test_help_action_improves_target_and_witness_relationships():
    simulation = create_default_street()

    simulate_player_action(simulation, action_kind="help", target_id="mira")

    mira_relationship = simulation.entities["mira"].relationship_to_player
    rook_relationship = simulation.entities["rook"].relationship_to_player

    assert mira_relationship.trust == 8
    assert mira_relationship.familiarity == 2
    assert rook_relationship.trust == 2
    assert rook_relationship.familiarity == 1


def test_harmful_actions_create_personal_fear_and_resentment():
    simulation = create_default_street()

    simulate_player_action(simulation, action_kind="assault", target_id="mira")
    simulate_player_action(simulation, action_kind="steal", target_id="rook")
    simulate_player_action(simulation, action_kind="threaten", target_id="mira")

    mira_relationship = simulation.entities["mira"].relationship_to_player
    rook_relationship = simulation.entities["rook"].relationship_to_player

    assert mira_relationship.fear == 15
    assert mira_relationship.resentment == 12
    assert rook_relationship.fear == 7
    assert rook_relationship.resentment == 9


def test_talk_action_increases_target_familiarity_and_trust():
    simulation = create_default_street()

    simulate_player_action(simulation, action_kind="talk", target_id="rook")

    relationship = simulation.entities["rook"].relationship_to_player
    assert relationship.familiarity == 3
    assert relationship.trust == 1


def test_high_trust_target_questions_threat_instead_of_calling_police():
    simulation = create_default_street()
    simulation.entities["mira"].relationship_to_player.trust = 8

    result = simulate_player_action(simulation, action_kind="threaten", target_id="mira")

    assert result.reactions_by_entity["mira"].actions == ("question",)


def test_high_fear_target_flees_without_calling_police():
    simulation = create_default_street()
    simulation.entities["mira"].relationship_to_player.fear = 10

    result = simulate_player_action(simulation, action_kind="threaten", target_id="mira")

    assert result.reactions_by_entity["mira"].actions == ("flee",)


def test_high_resentment_witness_confronts_harmful_event():
    simulation = create_default_street()
    simulation.entities["rook"].relationship_to_player.resentment = 8

    result = simulate_player_action(simulation, action_kind="threaten", target_id="mira")

    assert result.reactions_by_entity["rook"].actions == ("confront",)


def test_high_trust_target_warmly_greets_player_in_conversation():
    simulation = create_default_street()
    simulation.entities["mira"].relationship_to_player.trust = 8

    result = simulate_player_action(simulation, action_kind="talk", target_id="mira")

    assert result.reactions_by_entity["mira"].actions == ("warmly_greet",)


def test_high_resentment_theft_target_confronts_player():
    simulation = create_default_street()
    simulation.entities["rook"].relationship_to_player.resentment = 8

    result = simulate_player_action(simulation, action_kind="steal", target_id="rook")

    assert result.reactions_by_entity["rook"].actions == ("confront",)


def test_reactions_include_dialogue_lines():
    simulation = create_default_street()

    result = simulate_player_action(simulation, action_kind="help", target_id="mira")

    assert result.reactions_by_entity["mira"].dialogue == "Thanks. I will remember that you helped me."


def test_simulation_accepts_dialogue_provider():
    class Provider:
        def generate(self, prompt):
            return "Generated from structured context."

    simulation = create_default_street()

    result = simulate_player_action(
        simulation,
        action_kind="help",
        target_id="mira",
        dialogue_provider=Provider(),
    )

    assert result.reactions_by_entity["mira"].dialogue == "Generated from structured context."


def test_simulation_accepts_decision_provider_for_npc_intent():
    class DecisionProvider:
        def generate(self, prompt):
            return (
                '{"action":"warn_player","target_id":"player",'
                '"reason":"Mira trusts the player but worries about police involvement.",'
                '"dialogue":"You keep helping people. Just be careful around Chen."}'
            )

    simulation = create_default_street()

    result = simulate_player_action(
        simulation,
        action_kind="help",
        target_id="officer_chen",
        decision_provider=DecisionProvider(),
    )

    assert result.reactions_by_entity["mira"].actions == ("warn_player",)
    assert result.reactions_by_entity["mira"].reason == "Mira trusts the player but worries about police involvement."
    assert result.reactions_by_entity["mira"].dialogue == "You keep helping people. Just be careful around Chen."
    assert result.reactions_by_entity["mira"].dialogue_source == "deepseek"
