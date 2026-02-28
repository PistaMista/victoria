import { expect, test, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/svelte";
import BackButton from "./BackButton.svelte";
import { goto } from "$app/navigation";

vi.mock("$app/navigation", () => ({
	goto: vi.fn(),
}));

test("back button routes to provided route on click", async () => {
	const user = userEvent.setup();
	const { getByRole } = render(BackButton, {
		route: "/my/fancy/route",
	});

	const button = getByRole("button");

	await user.click(button);

	expect(goto).toBeCalledWith("/my/fancy/route");
});
