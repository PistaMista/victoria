import { expect, test } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/svelte";
import AgentStatusIndicator from "./AgentStatusIndicator.svelte";

test("agent status indicator displays given agent status", async () => {
	const { container } = render(AgentStatusIndicator, {
		status: "BUSY",
	});

	expect(container).toHaveTextContent("BUSY");
});
