from neon_agency.simulation import simulate_player_assault


HELP_TEXT = """Available commands:
- help
- status
- attack <entity_id>
- memories <entity_id>
- quit"""


def handle_command(simulation, command):
    parts = command.strip().split()
    if not parts:
        return ""

    name = parts[0].lower()
    if name == "help":
        return HELP_TEXT
    if name == "status":
        return format_status(simulation)
    if name == "attack":
        return _handle_entity_command(simulation, parts, _attack_entity)
    if name == "memories":
        return _handle_entity_command(simulation, parts, _format_entity_memories)
    if name in {"quit", "exit"}:
        return "Goodbye."
    return f"Unknown command: {name}\nType 'help' to see available commands."


def run_shell(input_func=input, output_func=print):
    simulation = None
    simulation = _create_simulation()
    output_func("Neon Agency interactive sandbox. Type 'help' for commands.")

    while True:
        try:
            command = input_func("> ")
        except EOFError:
            output_func("Goodbye.")
            return

        output = handle_command(simulation, command)
        if output:
            output_func(output)
        if command.strip().lower() in {"quit", "exit"}:
            return


def format_status(simulation):
    lines = [
        "City reputation:",
        f"- player_violence_score: {simulation.city_reputation.player_violence_score}",
        f"- police_attention: {simulation.city_reputation.police_attention}",
        "",
        "Entities:",
    ]
    for entity_id, entity in simulation.entities.items():
        lines.append(f"- {entity_id}: {entity.name} ({entity.role})")
    return "\n".join(lines)


def format_assault_result(simulation, result):
    target = simulation.entities[result.event.target_id]
    lines = [
        f"Action: attack {target.name}",
        f"{target.name} was attacked by {result.event.actor_id}.",
        "",
        "Reactions:",
    ]
    for reaction in result.reactions_by_entity.values():
        entity = simulation.entities[reaction.entity_id]
        actions = " + ".join(reaction.actions)
        lines.append(f"- {entity.name} chooses: {actions} ({reaction.reason})")
    lines.extend(
        [
            "",
            "City reputation updated:",
            f"- player_violence_score: {simulation.city_reputation.player_violence_score}",
            f"- police_attention: {simulation.city_reputation.police_attention}",
        ]
    )
    return "\n".join(lines)


def _handle_entity_command(simulation, parts, handler):
    if len(parts) != 2:
        return f"Usage: {parts[0]} <entity_id>"
    entity_id = parts[1].lower()
    if entity_id not in simulation.entities or entity_id == "player":
        return f"Unknown entity: {entity_id}"
    return handler(simulation, entity_id)


def _attack_entity(simulation, entity_id):
    result = simulate_player_assault(simulation, target_id=entity_id)
    return format_assault_result(simulation, result)


def _format_entity_memories(simulation, entity_id):
    entity = simulation.entities[entity_id]
    lines = [f"Memories for {entity.name}:"]
    if not entity.memories:
        lines.append("- No memories yet.")
        return "\n".join(lines)

    for memory in entity.memories:
        lines.append(f"- {memory.perception} {memory.event_kind} by {memory.actor_id} against {memory.target_id}")
    return "\n".join(lines)


def _create_simulation():
    from neon_agency.simulation import create_default_street

    return create_default_street()
