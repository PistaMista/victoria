import { expect, test } from "vitest";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";
import { render, waitFor } from "@testing-library/svelte";
import ChatListItem from "./ChatListItem.svelte";
import { goto } from "$app/navigation";

vi.mock("$app/navigation", () => ({
  goto: vi.fn(),
}));

test("chat list item shows title of given chat", async () => {
  const { baseElement } = render(ChatListItem, {
    chat: {
      id: 1,
      title: "Cooking soup",
      summary: "How do I cook soup?",
      rootExchangeId: 1,
    },
  });

  expect(baseElement).toHaveTextContent("Cooking soup");
});

test("chat list item shows summary of given chat", async () => {
  const { baseElement } = render(ChatListItem, {
    chat: {
      id: 10,
      title: "Exterminating bugs",
      summary: "How does one exterminate bugs?",
      rootExchangeId: 1,
    },
  });

  expect(baseElement).toHaveTextContent("How does one exterminate bugs?");
});

test("clicking chat list item routes to the chat view for the given chat", async () => {
  const user = userEvent.setup();
  const { getByRole } = render(ChatListItem, {
    chat: {
      id: 21,
      title: "Not building shelves",
      summary: "Help I accidentally built a shelf!",
      rootExchangeId: 1,
    },
  });

  const button = getByRole("button");
  user.click(button);

  await waitFor(() => {
    expect(goto).toBeCalledWith("/chats/21");
  });
});
