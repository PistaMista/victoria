import { expect, test } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen, within } from "@testing-library/svelte";
import Component from "./MarkdownContent.svelte";
import { MarkdownContent } from "$lib/types/message";

const content: MarkdownContent = {
	type: "markdown",
	markdownText: "This is **bold**",
};

test("markdown message with bold text contains b tag", async () => {
	const { container } = render(Component, {
		content: content,
	});

	const bold = container.querySelector("strong");
	expect(bold).toBeInTheDocument();
});
