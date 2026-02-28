import { expect, test, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/svelte";
import CreateButton from "./CreateButton.svelte";

test("create button executes provided callback on click", async () => {
  const user = userEvent.setup();
  const callback = vi.fn();
  const { getByRole } = render(CreateButton, {
    onclick: callback,
  });

  const button = getByRole("button");
  await user.click(button);

  expect(callback).toBeCalled();
});
