import { ConnectionListItem, type Connection } from "$lib/types/connection";
import { Connection as ConnectionSchema, ConnectionListItem as ConnectionListItemSchema } from "$lib/types/connection";
import type { Diff } from "$lib/types/diff";
import { z } from "zod";


export async function listConnections(): Promise<ConnectionListItem[]> {
    const res = await fetch(`/api/connections`, {
        method: 'GET'
    });
    const json = await res.json();

    return z.array(ConnectionListItemSchema).parse(json);
}

export async function getConnection(id: number): Promise<Connection> {
    const res = await fetch(`/api/connections/${id}`, {
        method: 'GET'
    });
    const json = await res.json();
    
    return ConnectionSchema.parse(json);
}

// TODO: Streamline PUT API endpoints returning either modified object or bool
// (or make them return nothing)
export async function updateConnection(id: number, changes: Diff<Connection>): Promise<boolean> {
    const res = await fetch(`/api/connections/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(changes)
    });
    const json = await res.json();

    return z.boolean().parse(json);
}

export async function deleteConnection(id: number): Promise<boolean> {
    const res = await fetch(`/api/connections/${id}`, {
        method: 'DELETE'
    });
    const json = await res.json();

    return z.boolean().parse(json);
}

export async function createConnection(newConnection: Connection): Promise<ConnectionListItem> {
    const res = await fetch(`/api/connections`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newConnection)
    });
    const json = await res.json();

    return ConnectionListItem.parse(json);
}