import { expect, test } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/svelte";
import AgentMiniCard from "./AgentMiniCard.svelte";
import type { AgentListItem } from "$lib/types/agent";

const testAgent: AgentListItem = {
	id: 1,
	name: "John",
	status: "BUSY",
};

test("agent mini card shows name of given agent", async () => {
	const { container } = render(AgentMiniCard, {
		agent: testAgent,
	});

	expect(container).toHaveTextContent("John");
});

test("agent mini card shows status of given agent", async () => {
	const { container } = render(AgentMiniCard, {
		agent: testAgent,
	});

	expect(container).toHaveTextContent("BUSY");
});
