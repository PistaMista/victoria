<script lang="ts">
    import type { Route } from "$lib/types/route";
    import NavbarItem from "./NavbarItem.svelte";
    import { Button } from "flowbite-svelte";
    import { BarsOutline } from "flowbite-svelte-icons";
    
    export let routes: Array<Route>;
</script>

<div class="flex bg-slate-300 border-b-2 border-orange-400">
    <nav class="hidden md:flex w-full border-inherit">
        {#each routes as route}
            <NavbarItem {route}/>
        {/each}
    </nav>

    <Button class="md:hidden hover:bg-slate-400 px-1 content-center">
        <BarsOutline/>
    </Button>
    
    <div class="grow"/>
    
    <!-- This is a UserAvatar -->
    <div class="hover:bg-slate-400 w-6 h-6 bg-orange-500 rounded-full m-0.5"/>
</div>

