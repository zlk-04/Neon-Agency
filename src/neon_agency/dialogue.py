def generate_dialogue(entity, event, reaction):
    actions = reaction.actions
    relationship = entity.relationship_to_player

    if "thank" in actions:
        return "Thanks. I will remember that you helped me."
    if "question" in actions:
        if relationship.trust >= 8:
            return "You helped me before. Why are you threatening me now?"
        return "Why are you doing this?"
    if "flee" in actions:
        return "Stay away from me."
    if "call_police" in actions:
        return "I am calling the police."
    if "confront" in actions:
        if event.kind == "steal":
            return "I am done letting this slide. Give it back."
        return "I am not ignoring this anymore."
    if "warmly_greet" in actions:
        return "It is good to see you."
    if "acknowledge" in actions:
        return "Hey."
    if "record_video" in actions:
        return "I am recording this."
    if "investigate" in actions:
        return "I need to know what happened here."
    if "approve" in actions:
        return "That was decent of you."
    return ""
