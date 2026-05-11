import sys

from neon_agency.cli import format_assault_result, run_shell
from neon_agency.simulation import create_default_street, simulate_player_assault


def main():
    if "--demo" not in sys.argv:
        run_shell()
        return

    simulation = create_default_street()
    result = simulate_player_assault(simulation, target_id="mira")

    print("Street initialized:")
    for entity in simulation.entities.values():
        print(f"- {entity.name} ({entity.role})")

    print()
    print(format_assault_result(simulation, result))


if __name__ == "__main__":
    main()
