<script>
    import UserAvatar from "$lib/components/indicators/UserAvatar.svelte";
    import { Button } from "flowbite-svelte";
    import { CogSolid } from "flowbite-svelte-icons";
</script>

<div class="flex flex-row">
    <UserAvatar/>
    <div class="mr-auto">Kryštof Albrecht</div>
    <div class="rounded-md bg-blue-500 px-1 mr-1 font-bold text-white">ADMIN</div>
    <Button class="w-6 h-6 p-0"><CogSolid/></Button>
</div>                        