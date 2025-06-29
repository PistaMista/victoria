import { expect, test } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen } from '@testing-library/svelte';

test.todo('typing in search bar changes prompt variable')

test.todo('pressing enter in search bar executes submit callback')

// The "debounce period" is the amount of time that has to pass after a key was released,
// until the typing callback is called - the timer is reset when typing
test.todo('typing in search bar faster than the debounce period DOES NOT execute typing callback')

test.todo('typing in search bar executes the typing callback after the debounce period')