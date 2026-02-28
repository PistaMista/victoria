import { expect, test, type Mock, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen, waitFor } from "@testing-library/svelte";
import { registerHandler } from "../../../mocks/handlers/auth";
import { get } from "svelte/store";
import { goto } from "$app/navigation";
import RegistrationView from "./RegistrationView.svelte";

vi.mock("$app/navigation", () => ({
	goto: vi.fn(),
}));

test("registration view sends correct register request", async () => {
	const user = userEvent.setup();
	const { findByLabelText } = render(RegistrationView);

	const usernameBox = await findByLabelText("Username");
	const passwordBox = await findByLabelText("Password");
	const registerButton = await findByLabelText("Register");

	await user.type(usernameBox, "lorien");
	await user.type(passwordBox, "testard");
	await user.click(registerButton);

	expect(registerHandler).toBeCalled();
	let body = await (registerHandler as Mock).mock.calls[0][0].request
		.clone()
		.json();

	expect(body).toMatchObject({
		username: "lorien",
		password: "testard",
	});
});

test("registration view redirects to login view after successful registration", async () => {
	const user = userEvent.setup();
	const { findByLabelText } = render(RegistrationView);

	const usernameBox = await findByLabelText("Username");
	const passwordBox = await findByLabelText("Password");
	const registerButton = await findByLabelText("Register");

	await user.type(usernameBox, "lorien");
	await user.type(passwordBox, "testard");
	await user.click(registerButton);

	await waitFor(() => {
		expect(goto).toBeCalledWith("/login");
	});
});
