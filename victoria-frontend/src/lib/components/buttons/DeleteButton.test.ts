import { expect, test, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/svelte";
import DeleteButton from "./DeleteButton.svelte";

test("delete button shows confirmation buttons on click", async () => {
	const user = userEvent.setup();
	const callback = vi.fn();
	const { getByRole, getByLabelText } = render(DeleteButton, {
		onclick: callback,
	});

	const button = getByRole("button");
	await user.click(button);

	const confirm_button = getByLabelText("Delete");
	const cancel_button = getByLabelText("Cancel");

	expect(confirm_button).toBeInTheDocument();
	expect(cancel_button).toBeInTheDocument();
});

test("delete button executes callback after clicking on confirm", async () => {
	const user = userEvent.setup();
	const callback = vi.fn();
	const { getByRole, getByLabelText } = render(DeleteButton, {
		onclick: callback,
	});

	const button = getByRole("button");
	await user.click(button);

	const confirm_button = getByLabelText("Delete");
	await user.click(confirm_button);

	expect(callback).toBeCalled();
});

test("delete button does not execute callback and hides menu after clicking on cancel", async () => {
	const user = userEvent.setup();
	const callback = vi.fn();
	const { getByRole, getByLabelText } = render(DeleteButton, {
		onclick: callback,
	});

	const button = getByRole("button");
	await user.click(button);

	const confirm_button = getByLabelText("Delete");
	const cancel_button = getByLabelText("Cancel");
	await user.click(cancel_button);

	expect(callback).not.toBeCalled();
	expect(confirm_button).not.toBeInTheDocument();
	expect(cancel_button).not.toBeInTheDocument();
});
