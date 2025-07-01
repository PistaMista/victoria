import { expect, test } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen } from '@testing-library/svelte';

// WARNING:
// Chat receivers are NOT an independent entity in the database - they are just a string
// property of chat triggers

test.todo('chat receiver dropdown shows default option as selected when first rendered')

test.todo('chat receiver dropdown shows all chat receivers when clicked')

test.todo('chat receiver dropdown sets chat receiver variable when an option is clicked')

test.todo('chat receiver dropdown shows clicked option as selected')