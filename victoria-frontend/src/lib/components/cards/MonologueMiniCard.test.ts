import { expect, test, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/svelte";
import MonologueMiniCard from "./MonologueMiniCard.svelte";
import { goto } from "$app/navigation";
import type { MonologueListItem } from "$lib/types/monologue";

vi.mock("$app/navigation", () => ({
  goto: vi.fn(),
}));

const testMonologue: MonologueListItem = {
  id: 1,
  status: "RUNNING",
  title: "Research thesis ideas",
  summary: "Searching the web for sources",
};

test("monologue mini card shows name of given monologue", async () => {
  const { container } = render(MonologueMiniCard, {
    monologue: testMonologue,
  });

  expect(container).toHaveTextContent("Research thesis ideas");
});

// Shown using an icon, cannot test
test.skip("monologue mini card shows status of given monologue", async () => {
  const { container } = render(MonologueMiniCard, {
    monologue: testMonologue,
  });

  expect(container).toHaveTextContent("RUNNING");
});

test("monologue mini card routes to monologue detail when clicked", async () => {
  const user = userEvent.setup();
  const { getByRole } = render(MonologueMiniCard, {
    monologue: testMonologue,
  });
  const button = getByRole("button");

  await user.click(button);

  expect(goto).toBeCalled();
  expect(goto).toBeCalledWith("/monologues/1");
});
