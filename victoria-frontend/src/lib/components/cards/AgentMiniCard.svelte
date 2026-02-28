<script lang="ts">
	import type { Agent, AgentListItem } from "$lib/types/agent";
	import { CheckOutline } from "flowbite-svelte-icons";
	import AgentStatusIndicator from "../indicators/AgentStatusIndicator.svelte";

	export let agent: AgentListItem | Agent;
</script>

<div class="flex bg-slate-400 p-1 rounded-md">
	{agent.name}
	<div class="grow mx-2" />
	<AgentStatusIndicator status={agent.status} />
</div>

