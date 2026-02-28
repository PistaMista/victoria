import { expect, test, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/svelte";
import ConnectionListItem from "./ConnectionListItem.svelte";
import { goto } from "$app/navigation";

vi.mock("$app/navigation", () => ({
  goto: vi.fn(),
}));

test("connection list item shows name of given LLM service connection", async () => {
  const { container } = render(ConnectionListItem, {
    connection: {
      id: 1,
      name: "Hetzner",
    },
  });
  expect(container).toHaveTextContent("Hetzner");
});

test("pressing configure button of connection list item routes to detail of given LLM service connection", async () => {
  const user = userEvent.setup();
  const { getByRole } = render(ConnectionListItem, {
    connection: {
      id: 1,
      name: "Lol",
    },
  });

  const button = getByRole("button");
  await user.click(button);

  expect(goto).toBeCalledWith("/admin/settings/connections/1/edit");
});
