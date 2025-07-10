<script lang="ts">
    import { Button } from "flowbite-svelte";
    import { PlusOutline } from "flowbite-svelte-icons";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import Loader from "../placeholders/Loader.svelte";
    import { listConnections } from "$lib/api/connection";
    import type { ConnectionListItem } from "$lib/types/connection";
    import ItemComponent from "./items/ConnectionListItem.svelte";
    
    let connections: ConnectionListItem[] = [];

    let dataPromise: Promise<any> = Promise.resolve();

    async function load() {
        connections = await listConnections();
    }

    onMount(() => {
        dataPromise = load();
    })
</script>

<div class="flex flex-col space-y-2">
    <div class="flex flex-row">
        <div class="font-bold">
            Connections
        </div>
        <Button 
            on:click={() => goto("/admin/settings/connections/add")}
            aria-label="Add connection" 
            class="ml-auto w-6 h-6 p-0"
        ><PlusOutline/></Button>
    </div>
    
    <div class="flex flex-col">
        <Loader
            promise={dataPromise}
            pendingMessage="Loading connections..."
            rejectMessage="Failed to load connections"
        >
            {#each connections as connection}
                <ItemComponent {connection} />
            {/each}
        </Loader>
    </div>
</div>