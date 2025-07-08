<script lang="ts">
    import { getChatReceivers } from "$lib/api/chatting";
    import { Button, Dropdown, DropdownItem } from "flowbite-svelte";
    import { ChevronDownOutline } from "flowbite-svelte-icons";
    import { onMount } from "svelte";
    
    export let chosenReceiver: string | null = null;

    let receivers: string[] = [];
    let dropdownOpen: boolean = false;

    onMount(async () => {
        receivers = await getChatReceivers();
        chosenReceiver = receivers.at(0) ?? null;
    })
</script>

<div {...$$restProps}>
    <Button class="flex flex-row w-full">{chosenReceiver ?? "Choose receiver..."}<ChevronDownOutline class="w-6 h-6"/></Button>
    <Dropdown bind:open={dropdownOpen}>
        {#each receivers as receiver}
            <DropdownItem
                aria-label={receiver}
                on:click={() => {
                    chosenReceiver = receiver;
                    dropdownOpen = false;
                }}
            >
                {receiver}
            </DropdownItem>
        {/each}
    </Dropdown>
</div>