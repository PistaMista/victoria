import { expect, test, type Mock } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, within, waitFor } from "@testing-library/svelte";
import MonologueListView from "./MonologueListView.svelte";
import { listMonologuesHandler } from "../../../mocks/handlers/monologues";

test("monologue list view contains all monologue titles", async () => {
  const { container } = render(MonologueListView);

  await waitFor(() => {
    // No filtering options by default
    expect(listMonologuesHandler).toBeCalled();
    expect(
      (listMonologuesHandler as Mock).mock.calls[0][0].request.url,
    ).not.toContain("=");

    expect(container).toHaveTextContent("Research thesis ideas");
    expect(container).toHaveTextContent("Generate recipes for the week");
  });
});

test("monologue list view can filter by trigger", async () => {
  const user = userEvent.setup();
  const { findByLabelText } = render(MonologueListView);
  const dropdown = await findByLabelText("Filter by trigger");

  const button = within(dropdown).getByRole("button");
  await user.click(button);

  const pollOption = await within(dropdown).findByLabelText(
    "Discord message received",
  );
  await user.click(pollOption);

  expect(listMonologuesHandler).toBeCalledTimes(3);
  expect(
    (listMonologuesHandler as Mock).mock.calls[2][0].request.url,
  ).toContain("trigger=4");

  // Can stop filtering by trigger
  // await user.click(button);

  const anyOption = await within(dropdown).findByLabelText("Any");
  await user.click(anyOption);

  expect(listMonologuesHandler).toBeCalledTimes(4);
  expect(
    (listMonologuesHandler as Mock).mock.calls[3][0].request.url,
  ).not.toContain("trigger=");
});

test("monologue list view can filter by monologue status", async () => {
  const user = userEvent.setup();
  const { findByLabelText } = render(MonologueListView);
  const dropdown = await findByLabelText("Filter by monologue status");

  const button = within(dropdown).getByRole("button");
  await user.click(button);

  const runningOption = await within(dropdown).findByLabelText("Running");
  await user.click(runningOption);

  expect(listMonologuesHandler).toBeCalledTimes(3);
  expect(
    (listMonologuesHandler as Mock).mock.calls[2][0].request.url,
  ).toContain("monologueStatus=RUNNING");

  // Can stop filtering by monologue status
  // await user.click(button);

  const anyOption = await within(dropdown).findByLabelText("Any");
  await user.click(anyOption);

  expect(listMonologuesHandler).toBeCalledTimes(4);
  expect(
    (listMonologuesHandler as Mock).mock.calls[3][0].request.url,
  ).not.toContain("monologueStatus=");
});

test("monologue list view can filter by assigned agent", async () => {
  const user = userEvent.setup();
  const { findByLabelText } = render(MonologueListView);
  const dropdown = await findByLabelText("Filter by assigned agent");

  const button = within(dropdown).getByRole("button");
  await user.click(button);

  const cookOption = await within(dropdown).findByLabelText("Cook");
  await user.click(cookOption);

  expect(listMonologuesHandler).toBeCalledTimes(3);
  expect(
    (listMonologuesHandler as Mock).mock.calls[2][0].request.url,
  ).toContain("assignedAgent=1");

  // Can stop filtering by assigned agent
  // await user.click(button);

  const anyOption = await within(dropdown).findByLabelText("Any");
  await user.click(anyOption);

  expect(listMonologuesHandler).toBeCalledTimes(4);
  expect(
    (listMonologuesHandler as Mock).mock.calls[3][0].request.url,
  ).not.toContain("assignedAgent=");
});

test("monologue list view can search for monologues", async () => {
  const user = userEvent.setup();
  const { findByRole } = render(MonologueListView);
  const searchBar = await findByRole("search");

  await user.click(searchBar);
  await user.keyboard("random");

  await waitFor(() => {
    expect(listMonologuesHandler).toBeCalledTimes(3);
    expect(
      (listMonologuesHandler as Mock).mock.calls[2][0].request.url,
    ).toContain("searchQuery=random");
  });
});
