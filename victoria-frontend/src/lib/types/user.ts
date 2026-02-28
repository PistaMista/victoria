import { z } from "zod";

export const Role = z.enum(["user", "admin"]);

export const UserListItem = z.object({
  id: z.number(),
  username: z.string(),
  role: Role,
});

export type UserListItem = z.infer<typeof UserListItem>;

export const User = z.object({
  id: z.number(),
  username: z.string(),
  // WARNING: THIS IS ONLY FOR SETTING A NEW PASSWORD FRONTEND->BACKEND, NEVER REPLY WITH THE PASSWORD OR ITS HASH!
  newPassword: z.string(),
  role: Role,
  permittedActions: z.array(z.number()),
  permittedTriggers: z.array(z.number()),
});

export type User = z.infer<typeof User>;
