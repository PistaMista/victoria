<script lang="ts">
    import { Button, Dropdown, DropdownItem } from "flowbite-svelte";
    import { ChevronDownOutline } from "flowbite-svelte-icons";
</script>

<div>
    <Button class="flex flex-row w-full">IDENTITY<ChevronDownOutline class="w-6 h-6"/></Button>
    <Dropdown>
        <DropdownItem>Identity</DropdownItem>
        <DropdownItem>JSON</DropdownItem>
        <DropdownItem>XML</DropdownItem>
    </Dropdown>
</div>
