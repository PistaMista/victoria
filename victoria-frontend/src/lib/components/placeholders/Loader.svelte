<script lang="ts">
    import { CloseOutline } from "flowbite-svelte-icons";
    import { Spinner } from "flowbite-svelte";

    export let promise: Promise<void>;
    export let pendingMessage: string;
    export let rejectMessage: string;
    
    let resolved: boolean = false;
    let error: string | null = null;
    
    promise
        .then(() => {
            resolved = true
        })
        .catch((e) => error = e.toString());
</script>

{#if resolved}
    <slot/>
{:else}
    <div class="m-2 p-auto border-slate-500 rounded-md">
        <div class="flex flex-col">
            {#if error}
                <div class="flex flex-row text-red-500 font-bold">
                    <CloseOutline/> {rejectMessage}
                </div>
                <div class="text-red-500">
                    {error}
                </div>
            {:else}
                <div class="flex flex-row text-yellow-700 font-bold">
                    <Spinner color="yellow"/> {pendingMessage}
                </div>
            {/if}
        </div>
    </div>
{/if}
