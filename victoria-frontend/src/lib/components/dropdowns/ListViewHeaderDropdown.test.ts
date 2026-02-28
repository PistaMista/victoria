import { expect, test } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen, waitFor } from "@testing-library/svelte";
import ListViewHeaderDropdown, {
	type Option,
} from "./ListViewHeaderDropdown.svelte";

test("list view dropdown does not show options by default", async () => {
	let { container } = render(ListViewHeaderDropdown, {
		title: "Houses",
		options: [
			{ displayName: "Thatched", ariaLabel: "Thatched", value: 1 },
			{ displayName: "Shotgun", ariaLabel: "Shotgun", value: 2 },
			{ displayName: "Tall", ariaLabel: "Tall", value: true },
		],
	});

	expect(container).not.toHaveTextContent("Thatched");
	expect(container).not.toHaveTextContent("Shotgun");
	expect(container).not.toHaveTextContent("Tall");
});

test("list view header dropdown shows set options when clicked", async () => {
	const user = userEvent.setup();
	const { getByRole, container } = render(ListViewHeaderDropdown, {
		title: "Houses",
		"aria-label": "Houses",
		options: [
			{ displayName: "Thatched", ariaLabel: "Thatched", value: 1 },
			{ displayName: "Shotgun", ariaLabel: "Shotgun", value: 2 },
			{ displayName: "Tall", ariaLabel: "Tall", value: true },
		],
	});

	const button = getByRole("button");
	user.click(button);

	await waitFor(() => {
		expect(container).toHaveTextContent("Thatched");
		expect(container).toHaveTextContent("Shotgun");
		expect(container).toHaveTextContent("Tall");
	});
});
