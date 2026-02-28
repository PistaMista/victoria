import { expect, test, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen, waitFor } from "@testing-library/svelte";
import ListViewHeaderSearchBar from "./ListViewHeaderSearchBar.svelte";

test("pressing enter in search bar executes submit callback", async () => {
	const callback = vi.fn((val) => { });
	const user = userEvent.setup();
	const { getByRole } = render(ListViewHeaderSearchBar, {
		onsubmit: callback,
	});

	const bar = getByRole("search");

	await user.click(bar);
	await user.keyboard("abc{Enter}");

	expect(callback).toBeCalled();
	expect(callback).toBeCalledWith("abc");
});

// The "debounce period" is the amount of time that has to pass after a key was released,
// until the typing callback is called - the timer is reset when typing
test("typing in search bar debounces", async () => {
	const callback = vi.fn((val) => { });
	const user = userEvent.setup();

	const { getByRole } = render(ListViewHeaderSearchBar, {
		ontype: callback,
		debounce: 30,
	});

	const bar = getByRole("search");
	await user.click(bar);
	await user.keyboard("abc");

	expect(callback).not.toHaveBeenCalled();

	await waitFor(
		() => {
			expect(callback).toBeCalled();
			expect(callback).toBeCalledWith("abc");
		},
		{ timeout: 60 },
	);
});
