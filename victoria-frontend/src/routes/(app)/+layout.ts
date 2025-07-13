import { redirect } from '@sveltejs/kit';
import { get } from 'svelte/store';
import { authToken } from '$lib/stores/auth';

export async function load() {
    const token = get(authToken);

    if (!token) {
        throw redirect(302, '/login')
    }
}