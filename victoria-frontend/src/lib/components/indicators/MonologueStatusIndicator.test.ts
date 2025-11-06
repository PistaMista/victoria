import { expect, test, vi } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen } from '@testing-library/svelte';
import MonologueStatusIndicator from "./MonologueStatusIndicator.svelte";

test('monologue status indicator displays given monologue status', async () => {
	const ver_running = render(MonologueStatusIndicator, {
		status: 'RUNNING'
	});
	const ver_pending = render(MonologueStatusIndicator, {
		status: 'PENDING'
	});
	const ver_success = render(MonologueStatusIndicator, {
		status: 'SUCCESS'
	});
	const ver_failure = render(MonologueStatusIndicator, {
		status: 'FAILURE'
	});

	const hor_running = render(MonologueStatusIndicator, {
		status: 'RUNNING',
		horizontal: true
	});
	const hor_pending = render(MonologueStatusIndicator, {
		status: 'PENDING',
		horizontal: true
	});
	const hor_success = render(MonologueStatusIndicator, {
		status: 'SUCCESS',
		horizontal: true
	});
	const hor_failure = render(MonologueStatusIndicator, {
		status: 'FAILURE',
		horizontal: true
	});

	expect(ver_running.container).toHaveTextContent('RUNNING');
	expect(ver_pending.container).toHaveTextContent('PENDING');
	expect(ver_success.container).toHaveTextContent('SUCCESS');
	expect(ver_failure.container).toHaveTextContent('FAILURE');

	expect(hor_running.container).toHaveTextContent('RUNNING');
	expect(hor_pending.container).toHaveTextContent('PENDING');
	expect(hor_success.container).toHaveTextContent('SUCCESS');
	expect(hor_failure.container).toHaveTextContent('FAILURE');
})

test('monologue status indicator can optionally display monologue runtime', async () => {
	// Mock the current date
	vi.spyOn(Date, 'now').mockReturnValue(Date.UTC(2025, 1, 1, 14, 19, 11) / 1000);

	const hor_off = render(MonologueStatusIndicator, {
		status: 'RUNNING',
		horizontal: true,
		startTimestamp: Date.UTC(2025, 1, 1, 10, 50) / 1000
	});
	const ver_off = render(MonologueStatusIndicator, {
		status: 'RUNNING',
		horizontal: false,
		startTimestamp: Date.UTC(2025, 1, 1, 10, 50) / 1000
	});

	const hor_on = render(MonologueStatusIndicator, {
		status: 'RUNNING',
		horizontal: true,
		startTimestamp: Date.UTC(2025, 1, 1, 10, 50) / 1000,
		displayRuntime: true
	});
	const ver_on = render(MonologueStatusIndicator, {
		status: 'RUNNING',
		horizontal: false,
		startTimestamp: Date.UTC(2025, 1, 1, 10, 50) / 1000,
		displayRuntime: true
	});

	// Expect no digits when not displaying runtime
	expect(hor_off.container.textContent).not.toMatch(/\d/);
	expect(ver_off.container.textContent).not.toMatch(/\d/);

	// Expect formatted runtime when displayRuntime is on
	expect(hor_on.container).toHaveTextContent("209m11s");
	expect(ver_on.container).toHaveTextContent("209m11s");
})

test('monologue status indicator can optionally display monologue launch date', async () => {
	const hor_off = render(MonologueStatusIndicator, {
		status: 'RUNNING',
		horizontal: true,
		startTimestamp: Date.UTC(2025, 0, 1, 10, 50) / 1000
	});
	const ver_off = render(MonologueStatusIndicator, {
		status: 'RUNNING',
		horizontal: false,
		startTimestamp: Date.UTC(2025, 0, 1, 10, 50) / 1000
	});

	const hor_on = render(MonologueStatusIndicator, {
		status: 'RUNNING',
		horizontal: true,
		startTimestamp: Date.UTC(2025, 0, 1, 10, 50) / 1000,
		displayStartDate: true
	});
	const ver_on = render(MonologueStatusIndicator, {
		status: 'RUNNING',
		horizontal: false,
		startTimestamp: Date.UTC(2025, 0, 1, 10, 50) / 1000,
		displayStartDate: true
	});

	// Expect no years when not displaying date
	expect(hor_off.container.textContent).not.toMatch(/\d\d\d\d/);
	expect(ver_off.container.textContent).not.toMatch(/\d\d\d\d/);

	// Expect formatted date in local time
	expect(hor_on.container).toHaveTextContent("2025/01/01 10:50");
	expect(ver_on.container).toHaveTextContent("2025/01/01 10:50");

})

test('monologue status indicator can optionally display monologue finish date', async () => {
	const hor_off = render(MonologueStatusIndicator, {
		status: 'SUCCESS',
		horizontal: true,
		startTimestamp: Date.UTC(2025, 1, 1, 10, 50) / 1000,
		endTimestamp: Date.UTC(2025, 1, 2, 11, 55)
	});
	const ver_off = render(MonologueStatusIndicator, {
		status: 'SUCCESS',
		horizontal: false,
		startTimestamp: Date.UTC(2025, 1, 1, 10, 50) / 1000,
		endTimestamp: Date.UTC(2025, 1, 2, 11, 55) / 1000
	});

	const hor_on = render(MonologueStatusIndicator, {
		status: 'SUCCESS',
		horizontal: true,
		startTimestamp: Date.UTC(2025, 1, 1, 10, 50) / 1000,
		endTimestamp: Date.UTC(2025, 1, 2, 11, 55) / 1000,
		displayEndDate: true
	});
	const ver_on = render(MonologueStatusIndicator, {
		status: 'SUCCESS',
		horizontal: false,
		startTimestamp: Date.UTC(2025, 1, 1, 10, 50) / 1000,
		endTimestamp: Date.UTC(2025, 1, 2, 11, 55) / 1000,
		displayEndDate: true
	});

	// Expect no years when not displaying end date
	expect(hor_off.container.textContent).not.toMatch(/\d\d\d\d/);
	expect(ver_off.container.textContent).not.toMatch(/\d\d\d\d/);
	expect(hor_off.container).not.toHaveTextContent("N/A");
	expect(ver_off.container).not.toHaveTextContent("N/A");

	// Expect formatted date in local time
	expect(hor_on.container).toHaveTextContent("2025/02/02 11:55");
	expect(ver_on.container).toHaveTextContent("2025/02/02 11:55");
})

test('monologue status indicator does not display finish date of unfinished monologues', async () => {
	const hor = render(MonologueStatusIndicator, {
		status: 'RUNNING',
		horizontal: true,
		startTimestamp: Date.UTC(2025, 1, 1, 10, 50) / 1000,
		endTimestamp: Date.UTC(2025, 1, 2, 11, 55) / 1000,
		displayEndDate: true
	});
	const ver = render(MonologueStatusIndicator, {
		status: 'RUNNING',
		horizontal: false,
		startTimestamp: Date.UTC(2025, 1, 1, 10, 50) / 1000,
		endTimestamp: Date.UTC(2025, 1, 2, 11, 55) / 1000,
		displayEndDate: true
	});

	// Expect no years
	expect(hor.container.textContent).not.toMatch(/\d\d\d\d/);
	expect(ver.container.textContent).not.toMatch(/\d\d\d\d/);

	expect(hor.container).toHaveTextContent('N/A');
	expect(ver.container).toHaveTextContent('N/A');
})
