import { expect, test } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen } from '@testing-library/svelte';

// The Chat window does not include the prompt! It just contains the messages

test.todo('chat window shows all the text from all messages of a given conversation')