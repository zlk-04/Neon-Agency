from neon_agency.models import Memory


def perceive_assault(simulation, event):
    perceptions = {}
    for entity_id, entity in simulation.entities.items():
        if entity_id == event.actor_id:
            continue

        perception = _perception_for(entity_id, entity, event)
        if perception is None:
            continue

        entity.memories.append(
            Memory(
                event_kind=event.kind,
                actor_id=event.actor_id,
                target_id=event.target_id,
                perception=perception,
                summary=f"{entity.name} {perception} assault by {event.actor_id} against {event.target_id}.",
            )
        )
        perceptions[entity_id] = perception
    return perceptions


def _perception_for(entity_id, entity, event):
    if entity_id == event.target_id:
        return "victim"
    if entity_id in event.direct_witness_ids:
        return "witnessed"
    if entity.is_police and entity.location == event.location:
        return "heard"
    return None
