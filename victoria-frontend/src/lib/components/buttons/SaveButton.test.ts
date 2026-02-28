import { expect, test, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/svelte";
import SaveButton from "./SaveButton.svelte";

test("save button executes provided callback on click", async () => {
  const user = userEvent.setup();
  const callback = vi.fn();
  const { getByRole } = render(SaveButton, {
    onclick: callback,
  });

  const button = getByRole("button");
  await user.click(button);

  expect(callback).toBeCalled();
});
