<script lang="ts">
	import Navbar from "$lib/components/navbar/Navbar.svelte";
	import type { Route } from "$lib/types/route";

	let routes: Array<Route> = [
		{ display_name: "Dashboard", route_path: "/" },
		{ display_name: "Chats", route_path: "/chats" },
		{ display_name: "Monologues", route_path: "/monologues" },
		//{display_name: "Tasks", route_path: "/tasks"},
		{ display_name: "Agents", route_path: "/agents" },
		//{display_name: "Knowledge", route_path: "/knowledge" },
		{ display_name: "Admin", route_path: "/admin" },
	];
</script>

<div class="flex flex-col inset-0 absolute overflow-hidden">
	<div>
		<Navbar {routes} />
	</div>
	<div class="grow min-w-0 min-h-0 overflow-hidden">
		<slot />
	</div>
</div>
