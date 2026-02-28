import { http, HttpResponse } from "msw";
import { UserListItem, User } from "$lib/types/user";
import { spy } from "../spy";

export const listUsersHandler = await spy(() => {
	return HttpResponse.json<Array<UserListItem>>([
		{
			id: 1,
			username: "krystof",
			role: "admin",
		},
	]);
});

export const createUserHandler = await spy(() => {
	return HttpResponse.json<UserListItem>({
		id: 2,
		username: "john",
		role: "user",
	});
});

export const getUserHandler = await spy(() => {
	return HttpResponse.json<User>({
		id: 1,
		username: "krystof",
		newPassword: "",
		role: "admin",
		permittedActions: [1, 2, 3],
		permittedTriggers: [1],
	});
});

export const updateUserHandler = await spy(() => {
	return HttpResponse.json<Boolean>(true);
});

export const deleteUserHandler = await spy(() => {
	return HttpResponse.json<Boolean>(true);
});

export const handlers = [
	http.get("/api/users", listUsersHandler),
	http.post("/api/users", createUserHandler),

	http.get("/api/users/:id", getUserHandler),
	http.put("/api/users/:id", updateUserHandler),
	http.delete("/api/users/:id", deleteUserHandler),
];
