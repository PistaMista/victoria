<!-- These "thought cards" should be collapsible - the thoughts can be quite long -->
<script lang="ts">
	import type { Thought } from "$lib/types/thought";
	import { DateTime } from "ts-luxon";
	import ActionContent from "./thoughts/ActionContent.svelte";
	import FailureContent from "./thoughts/FailureContent.svelte";
	import SuccessContent from "./thoughts/SuccessContent.svelte";
	import TriggerContent from "./thoughts/TriggerContent.svelte";
	import VerbatimContent from "./thoughts/VerbatimContent.svelte";
	import { ReplyAllSolid } from "flowbite-svelte-icons";

	export let thought: Thought;
</script>

<div class="rounded-md z-20 bg-slate-200 p-2">
	<div class="float-right ml-auto">
		{DateTime.fromSeconds(thought.startTimestamp)
			.toLocal()
			.toFormat("yyyy/MM/dd HH:mm")}
	</div>
	{#if thought.invocation.type === "ActionInvocation"}
		<ActionContent content={thought.invocation} />
	{:else if thought.invocation.type === "ThoughtInvocation"}
		<VerbatimContent content={thought.invocation} />
	{:else if thought.invocation.type === "TriggerInvocation"}
		<TriggerContent content={thought.invocation} />
	{:else if thought.invocation.type === "SuccessInvocation"}
		<SuccessContent />
	{:else if thought.invocation.type === "FailureInvocation"}
		<FailureContent />
	{/if}

	{#if thought.result.length > 0}
		<div class="w-full border-t-2 border-slate-500">
			<ReplyAllSolid class="float-left mr-2" />
			{thought.result}
		</div>
	{/if}
</div>

