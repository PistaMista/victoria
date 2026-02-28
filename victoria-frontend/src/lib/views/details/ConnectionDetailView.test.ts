import { expect, test, type Mock } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen, waitFor } from "@testing-library/svelte";
import ConnectionDetailView from "./ConnectionDetailView.svelte";
import {
	createConnectionHandler,
	deleteConnectionHandler,
	getConnectionHandler,
	updateConnectionHandler,
} from "../../../mocks/handlers/connections";

test("connection detail shows details of Ollama connection", async () => {
	const { findByLabelText } = render(ConnectionDetailView, {
		id: 1,
	});

	// TODO: Show the API key of the connection as well
	const urlBox = (await findByLabelText("URL")) as HTMLInputElement;
	const nameBox = (await findByLabelText("Name")) as HTMLInputElement;

	// TODO: Fields should not be shown unless data is loaded!
	await waitFor(() => {
		expect(getConnectionHandler).toBeCalled();
	});

	expect(nameBox.value).toBe("Homelab");
	expect(urlBox.value).toBe("http://golem:11434");
});

test("connection detail can edit URL of Ollama connection", async () => {
	const user = userEvent.setup();
	const { findByLabelText } = render(ConnectionDetailView, {
		id: 1,
	});

	const nameBox = (await findByLabelText("Name")) as HTMLInputElement;
	const saveButton = await findByLabelText("Save connection");

	// TODO: Fields should not be shown unless data is loaded!
	await waitFor(() => {
		expect(getConnectionHandler).toBeCalled();
	});

	await user.clear(nameBox);
	await user.type(nameBox, "Hetzner?");
	await user.click(saveButton);

	expect(updateConnectionHandler).toBeCalled();
	let body = await (
		updateConnectionHandler as Mock
	).mock.calls[0][0].request.json();

	expect(body).toHaveProperty("name", "Hetzner?");
	expect(body).not.toHaveProperty("url");
});

test("connection detail can delete given Ollama connection", async () => {
	const user = userEvent.setup();
	const { findByLabelText } = render(ConnectionDetailView, {
		id: 1,
	});

	const deleteButton = await findByLabelText("Delete connection");

	// TODO: Fields should not be shown unless data is loaded!
	await waitFor(() => {
		expect(getConnectionHandler).toBeCalled();
	});

	await user.click(deleteButton);

	expect(deleteConnectionHandler).toBeCalled();
	expect(
		(deleteConnectionHandler as Mock).mock.calls[0][0].request.url,
	).toContain("/api/connections/1");
});

test("connection detail can create new Ollama connection (given no id)", async () => {
	const user = userEvent.setup();
	const { findByLabelText } = render(ConnectionDetailView, {
		id: null,
	});

	{
		// Name
		const nameBox = (await findByLabelText("Name")) as HTMLInputElement;
		await user.clear(nameBox);
		await user.type(nameBox, "Vercel");
	}

	{
		// URL
		const urlBox = (await findByLabelText("URL")) as HTMLInputElement;
		await user.clear(urlBox);
		await user.type(urlBox, "https://lol.com:11434");
	}

	{
		// Create
		const createButton = await findByLabelText("Create connection");
		await user.click(createButton);
	}

	expect(createConnectionHandler).toBeCalled();
	let body = await (
		createConnectionHandler as Mock
	).mock.calls[0][0].request.json();

	expect(body).toHaveProperty("name", "Vercel");
	expect(body).toHaveProperty("url", "https://lol.com:11434");
});
