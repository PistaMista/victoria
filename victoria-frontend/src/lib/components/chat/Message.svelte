<script lang="ts">
	import ActionConfirmationContent from "./messages/ActionConfirmationContent.svelte";
	import MarkdownContent from "./messages/MarkdownContent.svelte";
	import ChoicePromptContent from "./messages/ChoicePromptContent.svelte";
	import ImageContent from "./messages/ImageContent.svelte";
	import type { Message } from "$lib/types/message";
	import { DateTime } from "ts-luxon";

	export let message: Message;
</script>

<div class="flex flex-col">
	<div class="flex flex-row">
		<div class="font-semibold mr-auto">{message.senderName}</div>
		<div class="text-gray-600 text-xs content-center">
			{DateTime.fromSeconds(message.timestamp)
				.toLocal()
				.toFormat("yyyy/MM/dd HH:mm")}
		</div>
	</div>

	{#if message.content.type === "action_confirmation"}
		<ActionConfirmationContent content={message.content} />
	{:else if message.content.type === "choice_prompt"}
		<ChoicePromptContent content={message.content} />
	{:else if message.content.type === "image"}
		<ImageContent content={message.content} />
	{:else if message.content.type === "markdown"}
		<MarkdownContent content={message.content} />
	{/if}
</div>
