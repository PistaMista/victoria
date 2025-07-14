<script lang="ts">
    import type { Route } from "$lib/types/route";
    import NavbarItem from "./NavbarItem.svelte";
    import { Drawer } from "flowbite-svelte";
    import { BarsOutline } from "flowbite-svelte-icons";
    
    export let routes: Array<Route>;
    
    let drawerHidden: boolean = true;
</script>

<div class="flex bg-slate-300 border-b-2 border-orange-400">
    <nav class="hidden md:flex w-full border-inherit">
        {#each routes as route}
            <NavbarItem {route}/>
        {/each}
    </nav>

    <button 
        aria-label="Open navigation drawer"
        on:click={() => drawerHidden = !drawerHidden} 
        class="md:hidden hover:bg-slate-400 px-1 content-center"
    >
        <BarsOutline/>
    </button>
    
    <div class="grow"/>
    
    <!-- This is a UserAvatar -->
    <div class="hover:bg-slate-400 w-6 h-6 bg-orange-500 rounded-full m-0.5"/>
</div>

<Drawer aria-label="Navigation drawer" bind:hidden={drawerHidden} placement="left">
    <nav class="flex flex-col">
        {#each routes as route}
            <NavbarItem {route}/>
        {/each}
    </nav>
</Drawer>