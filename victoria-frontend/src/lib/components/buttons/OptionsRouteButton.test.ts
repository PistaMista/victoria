import { expect, test, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/svelte";
import OptionsRouteButton from "./OptionsRouteButton.svelte";
import { CogSolid } from "flowbite-svelte-icons";
import { goto } from "$app/navigation";

vi.mock("$app/navigation", () => ({
  goto: vi.fn(),
}));

test("options route button routes to provided route on click", async () => {
  const user = userEvent.setup();
  const { getByRole } = render(OptionsRouteButton, {
    icon: CogSolid,
    text: "GO!",
    route: "/my/fancy/route",
  });

  const button = getByRole("button");

  await user.click(button);

  expect(goto).toBeCalledWith("/my/fancy/route");
});
