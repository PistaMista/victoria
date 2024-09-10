<script lang="ts">
    import { onMount } from 'svelte';

    let data = {
        data: "Loading..."
    };
    let error = null;

    onMount(async () => {
        try {
            const res = await fetch('/api/test');

            if (!res.ok) {
                throw new Error("API error");
            }

            data = await res.json();
        } catch (err: any) {
            error = err.message;
        }
    });
</script>

<h1>Welcome to SvelteKit!!!</h1>
<p>Visit <a href="https://kit.svelte.dev">KIT.SVELTE.DEV</a> to read the documentation</p>
<p>{data.data}</p>
