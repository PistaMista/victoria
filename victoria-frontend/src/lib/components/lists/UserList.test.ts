import { expect, test, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen, waitFor } from "@testing-library/svelte";
import { goto } from "$app/navigation";
import UserList from "./UserList.svelte";

vi.mock("$app/navigation", () => ({
	goto: vi.fn(),
}));

test("user list shows all usernames", async () => {
	const { container } = render(UserList);

	await waitFor(() => {
		expect(container).toHaveTextContent("krystof");
	});
});

test("pressing add button in user list routes to the user create view", async () => {
	const user = userEvent.setup();
	const { getByLabelText } = render(UserList);

	const button = getByLabelText("Create user");
	await user.click(button);

	expect(goto).toBeCalledWith("/admin/users/add");
});
