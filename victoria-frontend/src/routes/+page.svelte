<script lang="ts">
    import PromptBox from '$lib/PromptBox.svelte';
    import ChatWindow from '$lib/ChatWindow.svelte';
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


<div class="flex flex-col absolute inset-0">
    <div class="grow">
        <ChatWindow/>
    </div>
    <div class="justify-end">
        <PromptBox/>
    </div>
</div>
