<script lang="ts">
    import { onMount } from 'svelte';
    import { Alert } from 'flowbite-svelte';

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

<div class="p-8">
    <Alert>
        <span class="font-bold">Info alert!</span>
        {data.data}
    </Alert>
</div>
