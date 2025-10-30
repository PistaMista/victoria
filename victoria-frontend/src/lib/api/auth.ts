import { z } from "zod";

export async function login(username: string, password: string): Promise<void> {
    const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });
    const json = await res.json();

    if (!res.ok) {
        throw Error(json);
    }
}

export async function register(username: string, password: string): Promise<void> {
    await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password  
        })
    })
}

export async function isLoggedIn(): Promise<bool> {
    const res = await fetch('/api/auth/me', { 
	  method: 'GET'
    });
    const json = await res.json();

    return res.ok;
}
