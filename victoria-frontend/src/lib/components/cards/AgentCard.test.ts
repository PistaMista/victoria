import { expect, test, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen, waitFor } from "@testing-library/svelte";
import AgentCard from "./AgentCard.svelte";
import type { AgentListItem } from "$lib/types/agent";
import { goto } from "$app/navigation";

vi.mock("$app/navigation", () => ({
  goto: vi.fn(),
}));

const testAgent: AgentListItem = {
  id: 2,
  name: "Cook",
  status: "BUSY",
};

test("agent card shows name of given agent", async () => {
  const { container } = render(AgentCard, {
    agent: testAgent,
  });

  expect(container).toHaveTextContent("Cook");
});

test("agent card shows status of given agent", async () => {
  const { container } = render(AgentCard, {
    agent: testAgent,
  });

  expect(container).toHaveTextContent("BUSY");
});

test("agent card shows monologue names of given agent", async () => {
  const { container } = render(AgentCard, {
    agent: testAgent,
  });

  await waitFor(() => {
    expect(container).toHaveTextContent("Research thesis ideas");
    expect(container).toHaveTextContent("Respond to user message");
  });
});

test("agent card routes to agent editing when context button is pressed", async () => {
  const user = userEvent.setup();
  const { getByLabelText } = render(AgentCard, {
    agent: testAgent,
  });
  const detailButton = getByLabelText("Cook agent detail");

  await user.click(detailButton);

  expect(goto).toBeCalledWith("/agents/2/edit");
});
