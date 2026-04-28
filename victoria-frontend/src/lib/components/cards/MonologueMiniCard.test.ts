import { expect, test, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen, waitFor } from "@testing-library/svelte";
import MonologueMiniCard from "./MonologueMiniCard.svelte";
import { goto } from "$app/navigation";

vi.mock("$app/navigation", () => ({
	goto: vi.fn(),
}));


test("monologue mini card shows name of given monologue", async () => {
	const { container } = render(MonologueMiniCard, {
		monologueId: 1,
	});

	await waitFor(() => {
		expect(container).toHaveTextContent("Research thesis ideas");
	});
});

// Shown using an icon, cannot test
test.skip("monologue mini card shows status of given monologue", async () => {
	const { container } = render(MonologueMiniCard, {
		monologueId: 1,
	});

	await waitFor(() => {
		expect(container).toHaveTextContent("RUNNING");
	});
});

test("monologue mini card routes to monologue detail when clicked", async () => {
	const user = userEvent.setup();
	const { getByRole } = render(MonologueMiniCard, {
		monologueId: 1,
	});
	const button = getByRole("button");

	await user.click(button);

	expect(goto).toBeCalled();
	expect(goto).toBeCalledWith("/monologues/1");
});
