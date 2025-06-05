<script lang="ts">
    import type { Route } from "$lib/types/route";
    import NavbarItem from "./NavbarItem.svelte";
    
    export let routes: Array<Route>;
</script>

<nav class="flex w-full bg-slate-300 border-b-2 border-orange-400">
    {#each routes as route}
        <NavbarItem {route}/>
    {/each}
</nav>