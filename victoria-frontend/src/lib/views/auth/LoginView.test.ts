import { expect, test, type Mock, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen, waitFor } from "@testing-library/svelte";
import LoginView from "./LoginView.svelte";
import { loginHandler } from "../../../mocks/handlers/auth";
import { get } from "svelte/store";
import { goto } from "$app/navigation";

vi.mock("$app/navigation", () => ({
	goto: vi.fn(),
}));

test("login view sends correct login request", async () => {
	const user = userEvent.setup();
	const { findByLabelText } = render(LoginView);

	const usernameBox = await findByLabelText("Username");
	const passwordBox = await findByLabelText("Password");
	const loginButton = await findByLabelText("Login");

	await user.type(usernameBox, "lorien");
	await user.type(passwordBox, "testard");
	await user.click(loginButton);

	expect(loginHandler).toBeCalled();
	let body = await (loginHandler as Mock).mock.calls[0][0].request
		.clone()
		.json();

	expect(body).toMatchObject({
		username: "lorien",
		password: "testard",
	});
});

test("login view redirects to dashboard view after successful login", async () => {
	const user = userEvent.setup();
	const { findByLabelText } = render(LoginView);

	const usernameBox = await findByLabelText("Username");
	const passwordBox = await findByLabelText("Password");
	const loginButton = await findByLabelText("Login");

	await user.type(usernameBox, "tester");
	await user.type(passwordBox, "lolec");
	await user.click(loginButton);

	await waitFor(() => {
		expect(goto).toBeCalledWith("/");
	});
});

test("login view displays error after unsucessful login", async () => {
	const user = userEvent.setup();
	const { findByLabelText, container } = render(LoginView);

	const usernameBox = await findByLabelText("Username");
	const passwordBox = await findByLabelText("Password");
	const loginButton = await findByLabelText("Login");

	await user.type(usernameBox, "tester");
	await user.type(passwordBox, "wrong!");
	await user.click(loginButton);

	await waitFor(() => {
		expect(container).toHaveTextContent("Failed to log in");
	});
});
