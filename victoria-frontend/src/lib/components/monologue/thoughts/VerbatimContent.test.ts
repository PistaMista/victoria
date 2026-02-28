import { expect, test } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/svelte";
import type { ThoughtInvocation } from "$lib/types/thought";
import VerbatimContent from "./VerbatimContent.svelte";

const invocation: ThoughtInvocation = {
	type: "ThoughtInvocation",
	name: null,
	parameters: {
		thought: "This is a thought!",
	},
};

test("verbatim thought content displays no text", async () => {
	const { container } = render(VerbatimContent, {
		content: invocation,
	});

	expect(container.textContent).toBe("");
});
