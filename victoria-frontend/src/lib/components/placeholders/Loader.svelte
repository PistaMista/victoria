<script lang="ts">
    import { CloseOutline } from "flowbite-svelte-icons";
    import { Spinner } from "flowbite-svelte";

    export let promise: Promise<any>;
    export let pendingMessage: string;
    export let rejectMessage: string;
    
    let error: string | null = null;
</script>

{#await promise}
    <div class="mx-auto my-2">
        <div>
            <div class="flex flex-row text-yellow-700 font-bold justify-center">
                <Spinner color="yellow" class="mr-2"/> {pendingMessage}
            </div>
        </div>
    </div>
{:then _} 
    <slot/>
{:catch err}
    <div class="mx-auto my-2">
        <div>
            <div class="flex flex-row text-red-500 font-bold justify-center">
                <CloseOutline class="mr-2"/> {rejectMessage}
            </div>
            <div class="text-red-500">
                {error}
            </div>
        </div>
    </div>
{/await}

<!-- {#if resolved}
{:else}
    <div class="mx-auto my-2">
        <div>
            {#if error}
                <div class="flex flex-row text-red-500 font-bold justify-center">
                    <CloseOutline class="mr-2"/> {rejectMessage}
                </div>
                <div class="text-red-500">
                    {error}
                </div>
            {:else}
                <div class="flex flex-row text-yellow-700 font-bold justify-center">
                    <Spinner color="yellow" class="mr-2"/> {pendingMessage}
                </div>
            {/if}
        </div>
    </div>
{/if} -->
