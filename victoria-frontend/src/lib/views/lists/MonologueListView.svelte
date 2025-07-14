<script lang="ts">
    import ListView from "../ListView.svelte";
    import ListViewHeaderSearchBar from "$lib/components/search/ListViewHeaderSearchBar.svelte";
    import ListViewHeaderDropdown, { type Option } from "$lib/components/dropdowns/ListViewHeaderDropdown.svelte";
    import ListItemComponent from "$lib/components/lists/items/MonologueListItem.svelte";
    import Loader from "$lib/components/placeholders/Loader.svelte";
    import type { MonologueListItem, MonologueStatus } from "$lib/types/monologue";
    import { onMount } from "svelte";
    import type { AgentListItem } from "$lib/types/agent";
    import { getCurrentUserAgents } from "$lib/api/agents";
    import type { TriggerListItem } from "$lib/types/trigger";
    import { getPermittedTriggers } from "$lib/api/triggers";
    import { getCurrentUserMonologues } from "$lib/api/monologues";
    
    let triggerOption: Option | null;
    let monologueStatusOption: Option | null;
    let assignedAgentOption: Option | null;
    let searchQuery: string = "";
    
    let mounted = false;
    
    let agents: AgentListItem[] = [];
    let triggers: TriggerListItem[] = [];
    let monologues: MonologueListItem[] = [];
    
    let initPromise: Promise<void> = Promise.resolve();
    let dataPromise: Promise<void> = Promise.resolve();
    
    async function init() {
        agents = await getCurrentUserAgents();
        triggers = await getPermittedTriggers();
    }
        
    onMount(async () => {
        mounted = true;
        initPromise = init();
    })
    
    $: if (mounted) {
        dataPromise = (async () => {
            let triggerId: number | null = triggerOption?.value;
            let status: MonologueStatus | null = monologueStatusOption?.value;
            let agent: number | null = assignedAgentOption?.value;
            let query: string | null = searchQuery ? searchQuery : null;
            
            monologues = await getCurrentUserMonologues(triggerId, status, agent, query);
        })();
    }
</script>

<Loader
    promise={initPromise}
    pendingMessage="Initializing..."
    rejectMessage="Failed to initialize monologue list"
>
<ListView>
    <svelte:fragment slot="header">
        <ListViewHeaderSearchBar
            ontype={(val) => searchQuery = val}
        />
        <div class="mx-2 content-center flex flex-row">
            <!-- Filter by trigger -->
            <ListViewHeaderDropdown 
                title="Trigger"
                aria-label="Filter by trigger"
                options={
                [
                    {displayName: 'Any', ariaLabel: 'Any', value: null},
                    ...triggers.map((val) => (
                        {displayName: val.name, ariaLabel: val.name, value: val.id}
                    ))
                ]   
                }
                bind:chosenOption={triggerOption}
            />
            <!-- Filter by monologue status -->
            <ListViewHeaderDropdown
                title="Status"
                aria-label="Filter by monologue status"
                options={
                    [
                        {displayName: 'Any', ariaLabel: 'Any', value: null},
                        {displayName: 'Pending', ariaLabel: 'Pending', value: 'PENDING'},
                        {displayName: 'Running', ariaLabel: 'Running', value: 'RUNNING'},
                        {displayName: 'Success', ariaLabel: 'Success', value: 'SUCCESS'},
                        {displayName: 'Failure', ariaLabel: 'Failure', value: 'FAILURE'},
                    ]
                }
                bind:chosenOption={monologueStatusOption}
            />
            <!-- Filter by assigned agent -->
            <ListViewHeaderDropdown
                title="Agent"
                aria-label="Filter by assigned agent"
                options={
                [
                    {displayName: 'Any', ariaLabel: 'Any', value: null},
                    ...agents.map((val) => (
                        {displayName: val.name, ariaLabel: val.name, value: val.id }
                    ))
                ]
                }
                bind:chosenOption={assignedAgentOption}
            />
        </div>
    </svelte:fragment>

    <svelte:fragment slot="items">
        <Loader
            promise={dataPromise}
            pendingMessage="Loading monologues..."
            rejectMessage="Failed to load monologues"
        >
            {#each monologues as monologue}
                <ListItemComponent
                    {monologue}
                /> 
            {/each}
        </Loader>
    </svelte:fragment> 
</ListView>
</Loader>