<script lang="ts">
    import type { Route } from "$lib/types/route";
    export let route: Route;
</script>

<a href={route.route_path} class="px-1 border-r-2 border-inherit hover:bg-slate-400 content-center">
    {route.display_name}
</a>

