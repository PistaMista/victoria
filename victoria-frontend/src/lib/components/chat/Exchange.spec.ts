import { expect, test } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen } from '@testing-library/svelte';

test.todo('exchange shows all text from messages of exchange with given id')

test.todo('clicking name of monologue at the bottom of exchange routes to the monologue detail')

test.todo('clicking button to edit user prompt begins editing the user prompt')

test.todo('exchange sends request to generate new exchange after user prompt editing finishes')

test.todo('exchange sends request to generate new exchange after clicking the regenerate button')

test.todo('numbers at bottom of exchange show number of currently selected exchange')

test.todo('numbers at bottom of exchange show the number of alternate exchanges at this level')

test.todo('can cycle between alternate exchanges when cycle buttons are pressed')

test.todo('exchange can have user message set to null (if initiated by the agent)')

test.todo('bottom buttons (regenerate, edit prompt, cycle) are not shown if user message is null')