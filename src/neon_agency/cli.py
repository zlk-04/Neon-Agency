from neon_agency.simulation import simulate_player_action


HELP_TEXT = """Available commands:
- help
- status
- attack <entity_id>
- help <entity_id>
- steal <entity_id>
- threaten <entity_id>
- talk <entity_id>
- memories <entity_id>
- relationship <entity_id>
- relationships
- quit"""


ACTION_COMMANDS = {
    "attack": "assault",
    "help": "help",
    "steal": "steal",
    "threaten": "threaten",
    "talk": "talk",
}


def handle_command(simulation, command, dialogue_provider=None):
    parts = command.strip().split()
    if not parts:
        return ""

    name = parts[0].lower()
    if name == "help" and len(parts) == 1:
        return HELP_TEXT
    if name == "status":
        return format_status(simulation)
    if name == "relationships":
        return format_relationships(simulation)
    if name in ACTION_COMMANDS:
        return _handle_entity_command(simulation, parts, _run_player_action, dialogue_provider=dialogue_provider)
    if name == "memories":
        return _handle_entity_command(simulation, parts, _format_entity_memories)
    if name == "relationship":
        return _handle_entity_command(simulation, parts, _format_entity_relationship)
    if name in {"quit", "exit"}:
        return "Goodbye."
    return f"Unknown command: {name}\nType 'help' to see available commands."


def run_shell(input_func=input, output_func=print):
    simulation = _create_simulation()
    dialogue_provider = create_dialogue_provider()
    output_func("Neon Agency interactive sandbox. Type 'help' for commands.")

    while True:
        try:
            command = input_func("> ")
        except EOFError:
            output_func("Goodbye.")
            return

        output = handle_command(simulation, command, dialogue_provider=dialogue_provider)
        if output:
            output_func(output)
        if command.strip().lower() in {"quit", "exit"}:
            return


def format_status(simulation):
    lines = [
        "City reputation:",
        f"- player_violence_score: {simulation.city_reputation.player_violence_score}",
        f"- player_kindness_score: {simulation.city_reputation.player_kindness_score}",
        f"- player_theft_score: {simulation.city_reputation.player_theft_score}",
        f"- police_attention: {simulation.city_reputation.police_attention}",
        f"- civilian_trust: {simulation.city_reputation.civilian_trust}",
        "",
        "Entities:",
    ]
    for entity_id, entity in simulation.entities.items():
        lines.append(f"- {entity_id}: {entity.name} ({entity.role})")
    return "\n".join(lines)


def format_action_result(simulation, result):
    target = simulation.entities[result.event.target_id]
    action = _display_action(result.event.kind)
    lines = [
        f"Action: {action} {target.name}",
        f"{target.name} experienced {result.event.kind} by {result.event.actor_id}.",
        "",
        "Reactions:",
    ]
    for reaction in result.reactions_by_entity.values():
        entity = simulation.entities[reaction.entity_id]
        actions = " + ".join(reaction.actions)
        lines.append(f"- {entity.name} chooses: {actions} ({reaction.reason})")
        if reaction.dialogue:
            lines.append(f'  {entity.name} says [{reaction.dialogue_source}]: "{reaction.dialogue}"')
            if reaction.dialogue_error:
                lines.append(f"  dialogue fallback: {reaction.dialogue_error}")
    lines.extend(
        [
            "",
            "City reputation updated:",
            f"- player_violence_score: {simulation.city_reputation.player_violence_score}",
            f"- player_kindness_score: {simulation.city_reputation.player_kindness_score}",
            f"- player_theft_score: {simulation.city_reputation.player_theft_score}",
            f"- police_attention: {simulation.city_reputation.police_attention}",
            f"- civilian_trust: {simulation.city_reputation.civilian_trust}",
        ]
    )
    return "\n".join(lines)


def format_assault_result(simulation, result):
    return format_action_result(simulation, result)


def format_relationships(simulation):
    lines = ["Relationships:"]
    for entity_id, entity in simulation.entities.items():
        if entity_id == "player":
            continue
        relationship = entity.relationship_to_player
        lines.append(
            f"- {entity_id}: trust={relationship.trust} "
            f"fear={relationship.fear} "
            f"resentment={relationship.resentment} "
            f"familiarity={relationship.familiarity}"
        )
    return "\n".join(lines)


def create_dialogue_provider(env_path=".env"):
    from neon_agency.config import load_deepseek_config
    from neon_agency.providers.deepseek import DeepSeekDialogueProvider

    config = load_deepseek_config(env_path)
    if config is None:
        return None
    return DeepSeekDialogueProvider(config)


def _handle_entity_command(simulation, parts, handler, dialogue_provider=None):
    if len(parts) != 2:
        return f"Usage: {parts[0]} <entity_id>"
    entity_id = parts[1].lower()
    if entity_id not in simulation.entities or entity_id == "player":
        return f"Unknown entity: {entity_id}"
    return handler(simulation, entity_id, parts[0].lower(), dialogue_provider=dialogue_provider)


def _run_player_action(simulation, entity_id, command_name, dialogue_provider=None):
    result = simulate_player_action(
        simulation,
        action_kind=ACTION_COMMANDS[command_name],
        target_id=entity_id,
        dialogue_provider=dialogue_provider,
    )
    return format_action_result(simulation, result)


def _format_entity_memories(simulation, entity_id, command_name=None, dialogue_provider=None):
    entity = simulation.entities[entity_id]
    lines = [f"Memories for {entity.name}:"]
    if not entity.memories:
        lines.append("- No memories yet.")
        return "\n".join(lines)

    for memory in entity.memories:
        lines.append(f"- {memory.perception} {memory.event_kind} by {memory.actor_id} against {memory.target_id}")
    return "\n".join(lines)


def _format_entity_relationship(simulation, entity_id, command_name=None, dialogue_provider=None):
    entity = simulation.entities[entity_id]
    relationship = entity.relationship_to_player
    return "\n".join(
        [
            f"Relationship for {entity.name}:",
            f"- trust: {relationship.trust}",
            f"- fear: {relationship.fear}",
            f"- resentment: {relationship.resentment}",
            f"- familiarity: {relationship.familiarity}",
        ]
    )


def _create_simulation():
    from neon_agency.simulation import create_default_street

    return create_default_street()


def _display_action(event_kind):
    if event_kind == "assault":
        return "attack"
    return event_kind
