import { expect, test, type Mock } from "vitest";
import userEvent from '@testing-library/user-event';
import { render, screen, waitFor, within } from '@testing-library/svelte';
import UserDetailView from "./UserDetailView.svelte";
import { createUserHandler, deleteUserHandler, getUserHandler, updateUserHandler } from "../../../mocks/handlers/users";

test('user detail shows username of given user', async () => {
    const { getByLabelText } = render(UserDetailView, {
        id: 1
    });

    // TODO: Fields should not be shown unless data is loaded
    await waitFor(() => {
        expect(getUserHandler).toBeCalled();
    })
    
    const nameBox = getByLabelText("Username") as HTMLInputElement;
    expect(nameBox.value).toBe("krystof");
})

test('user detail can edit username of given user', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(UserDetailView, {
        id: 1
    });

    // TODO: Fields should not be shown unless data is loaded
    await waitFor(() => {
        expect(getUserHandler).toBeCalled();
    })
    
    const nameBox = getByLabelText("Username") as HTMLInputElement;
    const saveButton = getByLabelText("Save user");

    await user.clear(nameBox);
    await user.type(nameBox, "Leon");
    await user.click(saveButton);

    expect(updateUserHandler).toBeCalled();
    let body = await (updateUserHandler as Mock).mock.calls[0][0].request.json();
    
    expect(body).toHaveProperty('username', "Leon");
    expect(body).not.toHaveProperty('newPassword');
})

test('user detail can set new password of given user', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(UserDetailView, {
        id: 1
    });

    // TODO: Fields should not be shown unless data is loaded
    await waitFor(() => {
        expect(getUserHandler).toBeCalled();
    })
    
    const passwordBox = getByLabelText("New password") as HTMLInputElement;
    const saveButton = getByLabelText("Save user");

    await user.clear(passwordBox);
    await user.type(passwordBox, "lolol");
    await user.click(saveButton);

    expect(updateUserHandler).toBeCalled();
    let body = await (updateUserHandler as Mock).mock.calls[0][0].request.json();
    
    expect(body).toHaveProperty('newPassword', "lolol");
    expect(body).not.toHaveProperty('username');
})

test('user detail can edit allowed actions of given user', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(UserDetailView, {
        id: 1
    });

    // TODO: Fields should not be shown unless data is loaded
    await waitFor(() => {
        expect(getUserHandler).toBeCalled();
    })
    
    {
        const thinkBox = getByLabelText("Think");
        const monologueBox = getByLabelText("Start monologue");

        await user.click(thinkBox);
        await user.click(monologueBox);
    }

    const saveButton = getByLabelText("Save user");
    await user.click(saveButton);

    expect(updateUserHandler).toBeCalled();
    let body = await (updateUserHandler as Mock).mock.calls[0][0].request.json();
    
    expect(body).toHaveProperty('permittedActions', [1]);
})

test('user detail can edit allowed triggers of given user', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(UserDetailView, {
        id: 1
    });

    // TODO: Fields should not be shown unless data is loaded
    await waitFor(() => {
        expect(getUserHandler).toBeCalled();
    })
    
    {
        const recipeBox = getByLabelText("Generate recipes");
        const newsBox = getByLabelText("Check news");
        const chatBox = getByLabelText("General chat messages");

        await user.click(recipeBox);
        await user.click(newsBox);
        await user.click(chatBox);
    }

    const saveButton = getByLabelText("Save user");
    await user.click(saveButton);

    expect(updateUserHandler).toBeCalled();
    let body = await (updateUserHandler as Mock).mock.calls[0][0].request.json();
    
    expect(body).toHaveProperty('permittedTriggers', [2, 3]);
})

test('user detail can delete given user', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(UserDetailView, {
        id: 1
    });

    // TODO: Buttons should not be shown unless data is loaded
    await waitFor(() => {
        expect(getUserHandler).toBeCalled();
    })
    
    const deleteButton = getByLabelText("Delete user");
    await user.click(deleteButton);

    expect(deleteUserHandler).toBeCalled();
    expect((deleteUserHandler as Mock).mock.calls[0][0].request.url).toContain("/api/users/1");
})

test('user detail can create new user (given no id)', async () => {
    const user = userEvent.setup();
    const { getByLabelText } = render(UserDetailView, {
        id: null
    });
    
    { // Name
        const nameBox = getByLabelText("Username") as HTMLInputElement;
        await user.clear(nameBox);
        await user.type(nameBox, "Marcus");
    }
    
    { // Password
        const passwordBox = getByLabelText("New password") as HTMLInputElement;
        await user.clear(passwordBox);
        await user.type(passwordBox, "correcthorsebatterystaple");
    }
    
    { // Admin role
        const adminBox = getByLabelText("Enable admin role");
        await user.click(adminBox);
    }
    
    { // Actions
        const thinkBox = getByLabelText("Think");
        const monologueBox = getByLabelText("Start monologue");

        await user.click(thinkBox);
        await user.click(monologueBox);
    }
    
    const createButton = getByLabelText("Create user");
    await user.click(createButton);

    expect(createUserHandler).toBeCalled();
    let body = await (createUserHandler as Mock).mock.calls[0][0].request.json();

    expect(body).toMatchObject({
        username: "Marcus",
        newPassword: "correcthorsebatterystaple",
        role: 'admin',
        permittedActions: [2, 3],
        permittedTriggers: []
    })
})