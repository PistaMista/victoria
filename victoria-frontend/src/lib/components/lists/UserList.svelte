<script lang="ts">
    import { Button } from "flowbite-svelte";
    import { PlusOutline } from "flowbite-svelte-icons";
    import ItemComponent from "./items/UserListItem.svelte";
    import { goto } from "$app/navigation"
    import type { UserListItem } from "$lib/types/user";
    import { onMount } from "svelte";
    import { listUsers } from "$lib/api/users";
    
    let users: UserListItem[] = [];

    onMount(async () => {
        users = await listUsers();
    })
</script>

<div class="flex flex-col space-y-2">
    <div class="flex flex-row">
        <Button 
            aria-label="Create user"
            on:click={() => goto('/admin/users/add')} 
            class="ml-auto w-6 h-6 p-0"
        ><PlusOutline/></Button>
    </div>
    
    <div class="flex flex-col">
        {#each users as user}
            <ItemComponent {user}/>
        {/each}
    </div>
</div>