import { expect, test } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/svelte";
import GeneralDropdown from "./GeneralDropdown.svelte";

test("general dropdown shows placeholder by default", async () => {
  const { container } = render(GeneralDropdown, {
    placeholder: "Select house...",
    "aria-label": "Houses",
    options: [
      { displayName: "Thatched", ariaLabel: "Thatched", value: 1 },
      { displayName: "Shotgun", ariaLabel: "Shotgun", value: 2 },
      { displayName: "Tall", ariaLabel: "Tall", value: true },
    ],
  });

  expect(container).toHaveTextContent("Select house...");
});

test("general dropdown closes and shows selected option when option is selected", async () => {
  const user = userEvent.setup();
  const { getByLabelText, getByRole, container } = render(GeneralDropdown, {
    placeholder: "Select house...",
    "aria-label": "Houses",
    options: [
      { displayName: "Thatched", ariaLabel: "Thatched", value: 1 },
      { displayName: "Shotgun", ariaLabel: "Shotgun", value: 2 },
      { displayName: "Tall", ariaLabel: "Tall", value: true },
    ],
  });

  const button = getByRole("button");
  await user.click(button);

  const option = getByLabelText("Shotgun");
  await user.click(option);

  expect(option).not.toBeInTheDocument();
  expect(container).not.toHaveTextContent("Thatched");
  expect(container).not.toHaveTextContent("Tall");

  expect(container).toHaveTextContent("Shotgun");
});

test("general dropdown shows set options when clicked", async () => {
  const user = userEvent.setup();
  const { getByRole, container } = render(GeneralDropdown, {
    placeholder: "Select house...",
    "aria-label": "Houses",
    options: [
      { displayName: "Thatched", ariaLabel: "Thatched", value: 1 },
      { displayName: "Shotgun", ariaLabel: "Shotgun", value: 2 },
      { displayName: "Tall", ariaLabel: "Tall", value: true },
    ],
  });

  const button = getByRole("button");
  await user.click(button);

  expect(container).toHaveTextContent("Thatched");
  expect(container).toHaveTextContent("Shotgun");
  expect(container).toHaveTextContent("Tall");
});
