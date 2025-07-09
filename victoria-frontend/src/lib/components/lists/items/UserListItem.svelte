<script lang="ts">
    import UserAvatar from "$lib/components/indicators/UserAvatar.svelte";
    import { Button } from "flowbite-svelte";
    import { CogSolid } from "flowbite-svelte-icons";
    import { goto } from "$app/navigation";
    import type { UserListItem } from "$lib/types/user";

    export let user: UserListItem;
</script>

<div class="flex flex-row">
    <UserAvatar/>
    <div class="mr-auto">{user.username}</div>
    <div class="rounded-md bg-blue-500 px-1 mr-1 font-bold text-white">{user.role}</div>
    <Button 
        on:click={() => goto(`/admin/users/${user.id}/edit`)}
        class="w-6 h-6 p-0"
    ><CogSolid/></Button>
</div>                        