<script lang="ts">
    import type { Route } from "$lib/types/route";
    export let route: Route;
    import { goto } from "$app/navigation";
</script>

<a role="link" aria-label={route.display_name} on:click={() => goto(route.route_path)} class="px-1 border-r-2 border-inherit hover:bg-slate-400 content-center">
    {route.display_name}
</a>

