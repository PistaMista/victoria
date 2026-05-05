import { expect, test, type Mock } from "vitest";
import userEvent from "@testing-library/user-event";
import {
	findByLabelText,
	render,
	screen,
	waitFor,
	within,
} from "@testing-library/svelte";
import AgentDetailView from "./AgentDetailView.svelte";
import {
	createAgentHandler,
	deleteAgentHandler,
	getAgentHandler,
	updateAgentHandler,
} from "../../../mocks/handlers/agents";
import type { HTMLImageElement } from "happy-dom";

test("agent detail shows basic info about given agent", async () => {
	const { findByLabelText } = render(AgentDetailView, {
		id: 1,
	});

	const nameBox = (await findByLabelText("Name")) as HTMLInputElement;
	const modelDropdown = await findByLabelText("Base model");
	const promptBox = (await findByLabelText(
		"System prompt",
	)) as HTMLInputElement;
	const temperatureBox = (await findByLabelText(
		"Temperature",
	)) as HTMLInputElement;
	const topKBox = (await findByLabelText("Top K")) as HTMLInputElement;

	await waitFor(() => {
		expect(getAgentHandler).toBeCalled();
	});

	expect(nameBox.value).toBe("Cook");
	expect(modelDropdown).toHaveTextContent("gemma3:12b");
	expect(promptBox.value).toBe(
		"You're a Cook that generates recipes for the week...",
	);
	expect(temperatureBox.value).toBe("0.5");
	expect(topKBox.value).toBe("0.2");
});

test("agent detail can edit agent thumbnail", async () => {
	const user = userEvent.setup();
	const { findByLabelText } = render(AgentDetailView, {
		id: 1,
	});
	const newImage = new File(["lol"], "image.png", { type: "image/png" });

	const imagePicker = await findByLabelText("Set agent thumbnail");
	await user.upload(imagePicker, newImage);

	const thumbnail = (await findByLabelText(
		"Agent thumbnail",
	)) as unknown as HTMLImageElement;
	expect(thumbnail.src).toBe("data:image/png;base64,bG9s");

	const saveButton = await findByLabelText("Save agent");
	await user.click(saveButton);

	expect(updateAgentHandler).toBeCalled();
	let body = await (updateAgentHandler as Mock).mock.calls[0][0].request.json();

	expect(body).toMatchObject({
		thumbnailDataURI: "data:image/png;base64,bG9s",
	});
});

test("agent detail can edit given agent params", async () => {
	const user = userEvent.setup();
	const { findByLabelText } = render(AgentDetailView, {
		id: 1,
	});

	// FIXME: Fields should not be accessible unless data has finished loading
	await waitFor(() => {
		expect(getAgentHandler).toBeCalled();
	});

	// Name
	{
		const nameBox = (await findByLabelText("Name")) as HTMLInputElement;
		await user.clear(nameBox);
		await user.type(nameBox, "John");
	}

	// Model
	{
		const modelDropdown = await findByLabelText("Base model");
		const button = within(modelDropdown).getByRole("button");

		await user.click(button);

		const option = await within(modelDropdown).findByLabelText("llama3.1:8b");
		await user.click(option);
	}

	// Temperature
	{
		const temperatureBox = await findByLabelText("Temperature");
		await user.clear(temperatureBox);
		await user.click(temperatureBox);
		await user.keyboard("0.95{Enter}");
	}

	// Actions
	{
		const startMonologue = await findByLabelText("Start monologue");
		await user.click(startMonologue);
	}

	const saveButton = await findByLabelText("Save agent");
	await user.click(saveButton);

	expect(updateAgentHandler).toBeCalled();
	expect((updateAgentHandler as Mock).mock.calls[0][0].request.url).toContain(
		"/api/agents/1",
	);

	let body = await (updateAgentHandler as Mock).mock.calls[0][0].request.json();

	expect(body).not.toHaveProperty("systemPrompt");
	expect(body).not.toHaveProperty("modelParameters.top_k");
	expect(body).not.toHaveProperty("enabledTriggers");

	expect(body).toMatchObject({
		name: "John",
		baseModelId: 2,
		modelParameters: {
			temperature: 0.95,
		},
		enabledActions: [1, 2, 3],
	});
});

test("agent detail can delete given agent", async () => {
	const user = userEvent.setup();
	const { findByLabelText, getByLabelText } = render(AgentDetailView, {
		id: 1,
	});

	const button = await findByLabelText("Delete agent");
	await user.click(button);
	const confirmButton = getByLabelText("Delete");
	await user.click(confirmButton);

	expect(deleteAgentHandler).toBeCalled();
	expect((deleteAgentHandler as Mock).mock.calls[0][0].request.url).contain(
		"/api/agents/1",
	);
});

test("agent detail can create a new agent (with no id given)", async () => {
	const user = userEvent.setup();
	const { findByLabelText } = render(AgentDetailView, {
		id: null,
	});

	// Name
	{
		const nameBox = (await findByLabelText("Name")) as HTMLInputElement;
		await user.clear(nameBox);
		await user.type(nameBox, "Victoria");
	}

	// Model
	{
		const modelDropdown = await findByLabelText("Base model");
		const button = within(modelDropdown).getByRole("button");

		await user.click(button);

		const option = await within(modelDropdown).findByLabelText("gemma3:12b");
		await user.click(option);
	}

	// Prompt
	{
		const promptBox = await findByLabelText("System prompt");
		await user.clear(promptBox);
		await user.type(promptBox, "You do it all!");
	}

	// Temperature
	{
		const temperatureBox = await findByLabelText("Temperature");
		await user.clear(temperatureBox);
		await user.click(temperatureBox);
		await user.keyboard("0.92{Enter}");
	}

	// Triggers
	{
		const newsBox = await findByLabelText("Check news");
		const discordBox = await findByLabelText("Discord message received");
		await user.click(newsBox);
		await user.click(discordBox);
	}

	// Actions
	{
		const thinkBox = await findByLabelText("Think");
		await user.click(thinkBox);
	}

	const createButton = await findByLabelText("Create agent");

	await user.click(createButton);

	expect(createAgentHandler).toBeCalled();
	let body = await (createAgentHandler as Mock).mock.calls[0][0].request.json();
	expect(body).toMatchObject({
		name: "Victoria",
		baseModelId: 1,
		systemPrompt: "You do it all!",
		modelParameters: {
			temperature: 0.92,
			top_k: 40,
		},
		enabledTriggers: [2, 4],
		enabledActions: [2],
	});
});
