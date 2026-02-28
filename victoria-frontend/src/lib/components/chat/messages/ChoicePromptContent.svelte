<script lang="ts">
	import { ExclamationCircleSolid } from "flowbite-svelte-icons";
	import { Button } from "flowbite-svelte";
	import type { ChoicePromptContent } from "$lib/types/message";
	import { getQueryAnswer, sendQueryAnswer } from "$lib/api/queries";
	import { onMount } from "svelte";
	import Loader from "$lib/components/placeholders/Loader.svelte";

	export let content: ChoicePromptContent;

	let answer: any;

	let sendAnswerPromise: Promise<any> = Promise.resolve();
	let loadAnswerPromise: Promise<any> = Promise.resolve();

	async function loadAnswer() {
		answer = await getQueryAnswer(content.queryId);
	}

	async function sendAnswer(answer: any) {
		await sendQueryAnswer(content.queryId, answer);
		loadAnswerPromise = loadAnswer();
	}

	onMount(() => {
		loadAnswerPromise = loadAnswer();
	});
</script>

<div class="flex flex-col">
	<div
		class="bg-gradient-to-tr from-red-500 to-orange-500 justify-center flex flex-row font-semibold rounded-md"
	>
		<ExclamationCircleSolid class="mt-0.5 mr-2" />
		CHOICE REQUIRED
		<ExclamationCircleSolid class="mt-0.5 ml-2" />
	</div>
	<div class="text-center">
		{content.prompt}
	</div>

	<Loader
		promise={loadAnswerPromise}
		pendingMessage="Loading existing answer..."
		rejectMessage="Failed to load existing answer"
	>
		<Loader
			promise={sendAnswerPromise}
			pendingMessage="Sending answer..."
			rejectMessage="Failed to send answer"
		>
			{#if answer === null}
				<div
					class="flex flex-col space-y-2 rounded-md p-2 m-1 bg-slate-500"
				>
					{#each content.choices as choice}
						<Button
							class="w-full"
							aria-label={JSON.stringify(
								choice.value,
							)}
							on:click={() =>
								(sendAnswerPromise = sendAnswer(
									choice.value,
								))}
							>{JSON.stringify(
								choice.value,
							)}</Button
						>
					{/each}
				</div>
			{:else}
				<div>
					Chosen: <span class="font-bold"
						>{JSON.stringify(answer)}</span
					>
				</div>
			{/if}
		</Loader>
	</Loader>
</div>

