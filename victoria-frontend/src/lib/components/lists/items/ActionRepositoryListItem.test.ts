import { expect, test, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/svelte";
import type { ActionRepository } from "$lib/types/action_repo";
import ActionRepositoryListItem from "./ActionRepositoryListItem.svelte";
import { goto } from "$app/navigation";

vi.mock("$app/navigation", () => ({
  goto: vi.fn(),
}));

const testRepository: ActionRepository = {
  id: 1,
  name: "My cool action repo",
  url: "https://landchad.net",
};

test("action repository list item shows action repository name of given action repository", async () => {
  const { container } = render(ActionRepositoryListItem, {
    repository: testRepository,
  });

  expect(container).toHaveTextContent("My cool action repo");
});

test("clicking action repository list item routes to action repository detail", async () => {
  const user = userEvent.setup();
  const { getByRole } = render(ActionRepositoryListItem, {
    repository: testRepository,
  });
  const button = getByRole("button");

  await user.click(button);

  expect(goto).toBeCalledWith("/admin/actions/1/edit");
});
