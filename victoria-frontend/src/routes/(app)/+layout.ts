import { redirect } from '@sveltejs/kit';
import { get } from 'svelte/store';
import { isLoggedIn } from '$lib/api/auth';

export async function load() {
    if (!isLoggedIn()) {
        throw redirect(302, '/login')
    }
}
