<script lang="ts">
    import { Button, Dropdown, DropdownItem } from "flowbite-svelte";
    import { ChevronDownOutline } from "flowbite-svelte-icons";
</script>

<div class="hover:bg-slate-300 p-1 rounded-md">
    <Button class="flex flex-row">Trigger<ChevronDownOutline class="w-6 h-6"/></Button>
    <Dropdown>
        <DropdownItem>Timer</DropdownItem>
        <DropdownItem>Chat Message</DropdownItem>
        <DropdownItem>Webhook</DropdownItem>
        <DropdownItem>Monologue success</DropdownItem>
    </Dropdown>
</div>
