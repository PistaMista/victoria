import { expect, test, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/svelte";
import DeleteButton from "./DeleteButton.svelte";

test("delete button executes provided callback on click", async () => {
	const user = userEvent.setup();
	const callback = vi.fn();
	const { getByRole } = render(DeleteButton, {
		onclick: callback,
	});

	const button = getByRole("button");
	await user.click(button);

	expect(callback).toBeCalled();
});
