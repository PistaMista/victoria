import { z } from "zod";
import type { User, UserListItem } from "$lib/types/user";
import {
  User as UserSchema,
  UserListItem as UserListItemSchema,
} from "$lib/types/user";
import type { Diff } from "$lib/types/diff";

export async function listUsers(): Promise<UserListItem[]> {
  const res = await fetch(`/api/users`, {
    method: "GET",
  });
  const json = await res.json();

  if (!res.ok) {
    throw Error(json.detail);
  }

  return z.array(UserListItemSchema).parse(json);
}

export async function getUser(id: number): Promise<User> {
  const res = await fetch(`/api/users/${id}`, {
    method: "GET",
  });
  const json = await res.json();

  if (!res.ok) {
    throw Error(json.detail);
  }

  return UserSchema.parse(json);
}

export async function createUser(user: User): Promise<UserListItem> {
  const res = await fetch("/api/users", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(user),
  });
  const json = await res.json();

  if (!res.ok) {
    throw Error(json.detail);
  }

  return UserListItemSchema.parse(json);
}

export async function deleteUser(id: number): Promise<void> {
  const res = await fetch(`/api/users/${id}`, {
    method: "DELETE",
  });
  const json = await res.json();

  if (!res.ok) {
    throw Error(json.detail);
  }
}

export async function updateUser(
  id: number,
  changes: Diff<User>,
): Promise<void> {
  const res = await fetch(`/api/users/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(changes),
  });
  const json = await res.json();

  if (!res.ok) {
    throw Error(json.detail);
  }
}
