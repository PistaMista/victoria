import { expect, test, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen } from "@testing-library/svelte";
import { Message } from "$lib/types/message";
import Component from "./Message.svelte";

const userMessage: Message = {
  id: 1,
  timestamp: Date.UTC(2025, 1, 1, 20, 0, 0) / 1000,
  senderName: "Krystof",
  content: {
    type: "markdown",
    markdownText: "Hello!",
  },
};
const agentMessage: Message = {
  id: 2,
  timestamp: Date.UTC(2024, 1, 2, 3, 4, 5) / 1000,
  senderName: "Librarian",
  content: {
    type: "markdown",
    markdownText: "Agent message!",
  },
};

test("user message shows name of user", async () => {
  const { container } = render(Component, {
    message: userMessage,
  });

  expect(container).toHaveTextContent("Krystof");
});

test("agent message shows name of agent", async () => {
  const { container } = render(Component, {
    message: agentMessage,
  });

  expect(container).toHaveTextContent("Librarian");
});

test("message shows full date of sending", async () => {
  // Mock the current date
  vi.spyOn(Date, "now").mockReturnValue(
    Date.UTC(2025, 1, 3, 14, 19, 11) / 1000,
  );

  const { container } = render(Component, {
    message: userMessage,
  });

  expect(container).toHaveTextContent("2025/02/01 20:00");
});

test("message shows text content", async () => {
  const { container } = render(Component, {
    message: userMessage,
  });

  expect(container).toHaveTextContent("Hello!");
});
