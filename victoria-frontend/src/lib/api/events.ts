import type { Event } from "$lib/types/event";
import { Event as EventSchema } from "$lib/types/event";


export async function getEvent(id: number): Promise<Event> {
    const res = await fetch(`/api/events/${id}`, {
        method: 'GET'
    });
    const json = await res.json();

    if (!res.ok) {
        throw Error(json);
    }
    
    return EventSchema.parse(json);
}