import { expect, test, type Mock } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, within, waitFor } from "@testing-library/svelte";
import ActionRepositoryDetailView from "./ActionRepositoryDetailView.svelte";
import {
	createActionRepoHandler,
	deleteActionRepoHandler,
	getActionRepoHandler,
	setActionRepoHandler,
} from "../../../mocks/handlers/action_repos";

test("action repository detail shows info about given repository", async () => {
	const { findByLabelText } = render(ActionRepositoryDetailView, {
		id: 1,
	});

	const nameField: HTMLInputElement = within(
		await findByLabelText("Name"),
	).getByRole("textbox");
	const urlField: HTMLInputElement = within(
		await findByLabelText("URL"),
	).getByRole("textbox");

	await waitFor(() => {
		// Name
		expect(nameField.value).toBe("Home assistant tools");
		// URL
		expect(urlField.value).toBe("http://golem/PistaMista/HA-tools.git");
	});
});

test("action repository detail can edit URL of given repository", async () => {
	const user = userEvent.setup();
	const { findByLabelText } = render(ActionRepositoryDetailView, {
		id: 1,
	});

	const urlField: HTMLInputElement = within(
		await findByLabelText("URL"),
	).getByRole("textbox") as HTMLInputElement;
	const saveButton = await findByLabelText("Save action repository");

	// TODO: This is just a temporary fix - the fields SHOULD NOT be visible when the data is being loaded!!!
	// FIXME: We need to prevent the user from editing the fields and pressing the delete/save buttons unless the data is loaded
	await waitFor(async () => {
		// Wait for the data to be loaded
		expect(getActionRepoHandler).toBeCalled();
	});

	await user.clear(urlField);
	await user.type(urlField, "mycoolurl");

	await user.click(saveButton);

	await waitFor(async () => {
		expect(setActionRepoHandler).toBeCalled();
	});

	let body = await (
		setActionRepoHandler as Mock
	).mock.calls[0][0].request.json();

	expect(body).toHaveProperty("url", "mycoolurl");
	expect(body).not.toHaveProperty("name");
});

test("action repository detail can edit name of given repository", async () => {
	const user = userEvent.setup();
	const { findByLabelText } = render(ActionRepositoryDetailView, {
		id: 1,
	});

	const nameField: HTMLInputElement = within(
		await findByLabelText("Name"),
	).getByRole("textbox");
	const saveButton = await findByLabelText("Save action repository");

	// TODO: This is just a temporary fix - the fields SHOULD NOT be visible when the data is being loaded!!!
	// FIXME: We need to prevent the user from editing the fields and pressing the delete/save buttons unless the data is loaded
	await waitFor(async () => {
		// Wait for the data to be loaded
		expect(getActionRepoHandler).toBeCalled();
	});

	await user.clear(nameField);
	await user.type(nameField, "myName");

	await user.click(saveButton);

	expect(setActionRepoHandler).toBeCalled();
	let body = await (
		setActionRepoHandler as Mock
	).mock.calls[0][0].request.json();

	expect(body).toHaveProperty("name", "myName");
	expect(body).not.toHaveProperty("url");
});

test("action repository detail can delete a given repository", async () => {
	const user = userEvent.setup();
	const { findByLabelText, getByLabelText } = render(ActionRepositoryDetailView, {
		id: 1,
	});

	const deleteButton = await findByLabelText("Delete action repository");
	await user.click(deleteButton);
	const confirmButton = getByLabelText("Delete");
	await user.click(confirmButton);

	expect(deleteActionRepoHandler).toBeCalled();
	expect(
		(deleteActionRepoHandler as Mock).mock.calls[0][0].request.url,
	).toContain("/api/action-repos/1");
});

test("action repository detail can create a new action repository (with no id given)", async () => {
	const user = userEvent.setup();
	const { findByLabelText } = render(ActionRepositoryDetailView, {
		id: null,
	});

	const nameField: HTMLInputElement = within(
		await findByLabelText("Name"),
	).getByRole("textbox");
	const urlField: HTMLInputElement = within(
		await findByLabelText("URL"),
	).getByRole("textbox");
	const createButton = await findByLabelText("Create action repository");

	await user.type(nameField, "Mega repository 5000");
	await user.type(urlField, "https://www.megaurl.com");

	await user.click(createButton);

	expect(createActionRepoHandler).toBeCalled();
	let body = await (
		createActionRepoHandler as Mock
	).mock.calls[0][0].request.json();
	expect(body).toMatchObject({
		name: "Mega repository 5000",
		url: "https://www.megaurl.com",
	});
});
