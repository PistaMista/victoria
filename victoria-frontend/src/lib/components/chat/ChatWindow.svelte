<script lang="ts">
    import { onDestroy, onMount } from "svelte";
    import { writable, type Writable } from "svelte/store";
    import ItemComponent from "./Exchange.svelte";
    import { startReceivingExchanges } from "$lib/api/chatting";
    import type { Exchange } from "$lib/types/exchange";
    
    export let id: number;

    let exchanges: Writable<Exchange[]> = writable<Exchange[]>([]);

    let abortController: AbortController = new AbortController();
    let receivePromise: Promise<any> = Promise.resolve();
    
    onMount(() => {
        receivePromise = startReceivingExchanges(id, exchanges, abortController.signal);
    })
    
    onDestroy(() => {
        abortController.abort();
    })
</script>

<div class="grow min-h-0 mb-2 overflow-y-scroll">
    <div class="flex flex-col md:w-2/3 mx-2 md:m-auto">
        {#each $exchanges as exchange}
            <ItemComponent {exchange}/>
        {/each}
    </div>
</div>