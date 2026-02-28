import { expect, test, vi } from "vitest";
import userEvent from "@testing-library/user-event";
import { render, screen, waitFor } from "@testing-library/svelte";
import Loader from "./Loader.svelte";
import LoaderTestbed from "./LoaderTestbed.svelte";

test("loader shows loading message when given promise is pending", async () => {
	const pending: Promise<void> = new Promise(() => { });
	const { container } = render(Loader, {
		pendingMessage: "Loading items...",
		rejectMessage: "Failed to load items",
		promise: pending,
	});

	await waitFor(() => {
		expect(container).toHaveTextContent("Loading items...");
		expect(container).not.toHaveTextContent("CHILD");
	});
});

test("loader shows error message when given promise rejects", async () => {
	const rejecting: Promise<void> = new Promise((resolve, reject) => {
		reject("err");
	});
	const { container } = render(Loader, {
		pendingMessage: "Loading items...",
		rejectMessage: "Failed to load items",
		promise: rejecting,
	});

	await waitFor(() => {
		expect(container).toHaveTextContent("Failed to load items");
		expect(container).not.toHaveTextContent("CHILD");
	});
});

test("loader shows children when given promise resolves", async () => {
	const { container } = render(LoaderTestbed);

	await waitFor(() => {
		expect(container).toHaveTextContent("CHILD");
		expect(container).not.toHaveTextContent("Failed to load items");
		expect(container).not.toHaveTextContent("Loading items...");
	});
});
