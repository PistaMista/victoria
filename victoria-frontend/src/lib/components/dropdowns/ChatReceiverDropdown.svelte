<script lang="ts">
    import { Button, Dropdown, DropdownItem } from "flowbite-svelte";
    import { ChevronDownOutline } from "flowbite-svelte-icons";
</script>

<div>
    <Button class="flex flex-row w-full">General<ChevronDownOutline class="w-6 h-6"/></Button>
    <Dropdown>
        <DropdownItem>General</DropdownItem>
        <DropdownItem>Technical</DropdownItem>
        <DropdownItem>Research</DropdownItem>
    </Dropdown>
</div>