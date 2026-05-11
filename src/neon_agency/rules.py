BASE_ACTIONS = {
    "acknowledge",
    "approve",
    "call_police",
    "confront",
    "fight_back",
    "flee",
    "ignore",
    "record_video",
    "thank",
}
POLICE_ACTIONS = BASE_ACTIONS | {"investigate"}


def allowed_actions_for(entity):
    if entity.is_police:
        return POLICE_ACTIONS
    return BASE_ACTIONS


def filter_allowed(entity, actions):
    allowed = allowed_actions_for(entity)
    return tuple(action for action in actions if action in allowed)
