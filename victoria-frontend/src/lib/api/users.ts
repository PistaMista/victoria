import { z } from "zod";
import type { User, UserListItem } from "$lib/types/user";
import { User as UserSchema, UserListItem as UserListItemSchema } from "$lib/types/user";
import type { Diff } from "$lib/types/diff";

export async function getUser(id: number): Promise<User> {
    const res = await fetch(`/api/users/${id}`, {
        method: 'GET'
    });
    const json = await res.json();
    
    return UserSchema.parse(json);
}

export async function createUser(user: User): Promise<UserListItem> {
    const res = await fetch('/api/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user)
    })
    const json = await res.json();

    return UserListItemSchema.parse(json);
}

export async function deleteUser(id: number): Promise<boolean> {
    const res = await fetch(`/api/users/${id}`, {
        method: 'DELETE'
    });
    const json = await res.json();

    return z.boolean().parse(json);
}

export async function updateUser(id: number, changes: Diff<User>) {
    const res = await fetch(`/api/users/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(changes)
    });
    const json = await res.json();

    return z.boolean().parse(json);
}