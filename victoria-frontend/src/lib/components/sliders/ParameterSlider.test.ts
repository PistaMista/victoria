import { expect, test } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen, waitFor } from '@testing-library/svelte';
import ParameterSlider from "./ParameterSlider.svelte";

test('parameter slider textbox shows current value', async () => {
    const { getByRole } = render(ParameterSlider, {
        label: "My parameter",
        fallback: 20.0,
        value: 15.5,
        max: 30.0,
        min: 0.0
    });

    const box: HTMLInputElement = getByRole('textbox') as HTMLInputElement;
    expect(box.value).toBe("15.5");
})

test('parameter slider resets to previous value when empty textbox is defocused', async () => {
    const user = userEvent.setup();
    const { getByRole } = render(ParameterSlider, {
        label: "My parameter",
        fallback: 20.0,
        value: 15.5,
        max: 30.0,
        min: 0.0
    });

    const box: HTMLInputElement = getByRole('textbox') as HTMLInputElement;

    await user.click(box);
    await user.keyboard("{Backspace}{Backspace}03");

    expect(box.value).toBe("1503");
    box.blur();
    
    await waitFor(() => {
        expect(box.value).toBe("15.5")
    })
})

test('parameter slider textbox value stays on submit', async () => {
    const user = userEvent.setup();
    const { getByRole } = render(ParameterSlider, {
        label: "My parameter",
        fallback: 20.0,
        value: 15.5,
        max: 3000.0,
        min: 0.0
    });

    const box: HTMLInputElement = getByRole('textbox') as HTMLInputElement;

    await user.click(box);
    await user.keyboard("{Backspace}{Backspace}03{Enter}");

    box.blur();
    expect(box.value).toBe("1503");
})

test('parameter slider textbox limits value to max', async () => {
    const user = userEvent.setup();
    const { getByRole } = render(ParameterSlider, {
        label: "My parameter",
        fallback: 20.0,
        value: 15.5,
        max: 30.0,
        min: 0.0
    });

    const box: HTMLInputElement = getByRole('textbox') as HTMLInputElement;

    await user.clear(box);

    await user.click(box);
    await user.keyboard("9999{Enter}");

    box.blur();
    expect(box.value).toBe("30");
})

test('parameter slider resets to default value when reset button is clicked', async () => {
    const user = userEvent.setup();
    const { getByRole } = render(ParameterSlider, {
        label: "My parameter",
        fallback: 19.0,
        value: 15.5,
        max: 30.0,
        min: 0.0
    });

    const box = getByRole('textbox') as HTMLInputElement;

    const resetButton = getByRole('button');
    await user.click(resetButton);

    expect(box.value).toBe("19");
})

test('dragging parameter slider all the way left sets minimum value', async () => {
    const { getByRole } = render(ParameterSlider, {
        label: "My parameter",
        fallback: 19.0,
        value: 15.5,
        max: 30.0,
        min: 1.0
    });
    
    const box = getByRole('textbox') as HTMLInputElement;
    const slider = getByRole('slider') as HTMLInputElement;

    slider.value = "-10.0";
    slider.dispatchEvent(new Event('input', { bubbles: true}));

    await waitFor(() => {
        expect(box.value).toBe("1");
    })
})

test('dragging parameter slider all the way right sets maximum value', async () => {
    const { getByRole } = render(ParameterSlider, {
        label: "My parameter",
        fallback: 19.0,
        value: 15.5,
        max: 30.0,
        min: 0.0
    });
    
    const box = getByRole('textbox') as HTMLInputElement;
    const slider = getByRole('slider') as HTMLInputElement;

    slider.value = "9999.0";
    slider.dispatchEvent(new Event('input', { bubbles: true}));

    await waitFor(() => {
        expect(box.value).toBe("30");

    })
})
