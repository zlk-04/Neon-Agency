from neon_agency.simulation import create_default_street, simulate_player_assault


def main():
    simulation = create_default_street()
    result = simulate_player_assault(simulation, target_id="mira")

    print("Street initialized:")
    for entity in simulation.entities.values():
        print(f"- {entity.name} ({entity.role})")

    print()
    print("Action: attack Mira")
    print(f"{result.event.target_id} was attacked by {result.event.actor_id}.")

    print()
    print("Reactions:")
    for reaction in result.reactions_by_entity.values():
        entity = simulation.entities[reaction.entity_id]
        actions = " + ".join(reaction.actions)
        print(f"- {entity.name} chooses: {actions} ({reaction.reason})")

    print()
    print("City reputation updated:")
    print(f"- player_violence_score: {simulation.city_reputation.player_violence_score}")
    print(f"- police_attention: {simulation.city_reputation.police_attention}")


if __name__ == "__main__":
    main()
