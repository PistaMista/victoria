<script lang="ts">
    import Navbar from "$lib/components/navbar/Navbar.svelte";
    import type { Route } from "$lib/types/route";
    
    let routes: Array<Route> = [
        {display_name: "Conversations", route_path: "/conversations"},
        {display_name: "Knowledge", route_path: "/knowledge" },
        {display_name: "Models", route_path: "/models"},
        {display_name: "Monologues", route_path: "/monologues"}
    ];
</script>

<div class="flex flex-col justify-start inset-0 absolute">
    <div>
        <Navbar {routes}/>
    </div>
    <div class="grow"> 
        <slot/>
    </div>
</div>
