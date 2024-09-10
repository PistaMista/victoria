<script lang="ts">
    import { onMount } from 'svelte';
    import { Datepicker } from 'flowbite-svelte';

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
    <Datepicker />
</div>
