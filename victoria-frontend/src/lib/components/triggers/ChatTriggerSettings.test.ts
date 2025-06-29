import { expect, test } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen } from '@testing-library/svelte';

// Chat receivers are NOT an independent entity in the database - they are just a string
// property of chat triggers
test.todo('chat trigger settings allows selecting existing chat receiver name')

test.todo('chat trigger settings allows specifying new chat receiver name')