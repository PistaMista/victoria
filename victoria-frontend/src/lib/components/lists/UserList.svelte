<script lang="ts">
    import { Button } from "flowbite-svelte";
    import { PlusOutline } from "flowbite-svelte-icons";
    import UserListItem from "./items/UserListItem.svelte";
</script>

<div class="flex flex-col space-y-2">
    <div class="flex flex-row">
        <Button class="ml-auto w-6 h-6 p-0"><PlusOutline/></Button>
    </div>
    
    <div class="flex flex-col">
        <UserListItem/>
    </div>
</div>