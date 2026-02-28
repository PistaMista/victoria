<script lang="ts">
	import { getPermittedActions } from "$lib/api/actions";
	import {
		createAgent,
		deleteAgent,
		getAgent,
		updateAgent,
	} from "$lib/api/agents";
	import { getEnabledModels } from "$lib/api/models";
	import { getPermittedTriggers } from "$lib/api/triggers";
	import CreateButton from "$lib/components/buttons/CreateButton.svelte";
	import DeleteButton from "$lib/components/buttons/DeleteButton.svelte";
	import SaveButton from "$lib/components/buttons/SaveButton.svelte";
	import GeneralDropdown, {
		type Option,
	} from "$lib/components/dropdowns/GeneralDropdown.svelte";
	import Loader from "$lib/components/placeholders/Loader.svelte";
	import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
	import ParameterSlider from "$lib/components/sliders/ParameterSlider.svelte";
	import Toggle from "$lib/components/toggles/Toggle.svelte";
	import type { Action } from "$lib/types/action";
	import type { Agent } from "$lib/types/agent";
	import { getDiff } from "$lib/types/diff";
	import type { TriggerListItem } from "$lib/types/trigger";
	import { convertToDataURI } from "$lib/util/file";
	import DetailView from "$lib/views/DetailView.svelte";
	import { Textarea, Button, Input } from "flowbite-svelte";
	import { onMount } from "svelte";

	export let id: number | null;

	let loadedAgent: Agent = {
		id: 0,
		name: "",
		thumbnailDataURI: null,
		status: "IDLE",
		baseModelId: 0,
		systemPrompt: "",
		modelParameters: {
			temperature: 1.0,
			top_k: 40,
		},
		enabledTriggers: [],
		enabledActions: [],
	};
	let modifiedAgent: Agent = loadedAgent;

	let modelDropdownOptions: Option[];
	let chosenModel: Option | null = null;

	let actions: [Action, boolean][] = [];
	let triggers: [TriggerListItem, boolean][] = [];

	$: modifiedAgent.baseModelId = chosenModel?.value;
	$: modifiedAgent.enabledActions = actions
		.filter(([_, e]) => e)
		.map(([v, _]) => v.id);
	$: modifiedAgent.enabledTriggers = triggers
		.filter(([_, e]) => e)
		.map(([v, _]) => v.id);
	$: changes = getDiff(loadedAgent, modifiedAgent);

	let initPromise: Promise<any> = Promise.resolve();
	let deletePromise: Promise<any> = Promise.resolve();
	let savePromise: Promise<any> = Promise.resolve();
	let createPromise: Promise<any> = Promise.resolve();

	async function loadAgent() {
		if (id !== null) {
			loadedAgent = await getAgent(id);
			modifiedAgent = structuredClone(loadedAgent);
		}
	}

	async function initModelOptions() {
		let models = await getEnabledModels();
		modelDropdownOptions = models.map((val) => ({
			displayName: val.name,
			ariaLabel: val.name,
			value: val.id,
		}));

		if (id !== null) {
			chosenModel =
				modelDropdownOptions
					.filter(
						(val) =>
							val.value === loadedAgent.baseModelId,
					)
					.at(0) ?? null;
		}
	}

	async function initActionToggles() {
		actions = (await getPermittedActions()).map((val) => [
			val,
			loadedAgent.enabledActions.includes(val.id),
		]);
	}

	async function initTriggerToggles() {
		triggers = (await getPermittedTriggers()).map((val) => [
			val,
			loadedAgent.enabledTriggers.includes(val.id),
		]);
	}

	async function init() {
		await loadAgent();
		await initModelOptions();
		await initActionToggles();
		await initTriggerToggles();
	}

	function onDelete() {
		deletePromise = deleteAgent(modifiedAgent.id);
	}

	function onSave() {
		savePromise = updateAgent(modifiedAgent.id, changes);
	}

	function onCreate() {
		createPromise = createAgent(modifiedAgent);
	}

	async function setThumbnail(event: Event) {
		const input = event.target as HTMLInputElement;
		if (!input.files?.[0]) return;
		modifiedAgent.thumbnailDataURI = await convertToDataURI(
			input.files[0],
		);
	}

	onMount(async () => {
		initPromise = init();
	});
</script>

<Loader
	promise={initPromise}
	pendingMessage="Initializing view..."
	rejectMessage="Failed to initialize view"
>
	<Loader
		promise={deletePromise}
		pendingMessage="Deleting agent..."
		rejectMessage="Failed to delete agent"
	>
		<Loader
			promise={savePromise}
			pendingMessage="Saving changes..."
			rejectMessage="Failed to save changes"
		>
			<Loader
				promise={createPromise}
				pendingMessage="Creating agent..."
				rejectMessage="Failed to create agent"
			>
				<DetailView title="{modifiedAgent.name} agent">
					<DetailViewSection title="Name">
						<Input
							aria-label="Name"
							bind:value={modifiedAgent.name}
						/>
					</DetailViewSection>

					<DetailViewSection title="Thumbnail">
						<!-- TODO: Factor this out into an image picker component -->
						<div class="place-self-center">
							{#if modifiedAgent.thumbnailDataURI}
								<img
									class="w-48 h-48 rounded-md"
									aria-label="Agent thumbnail"
									src={modifiedAgent.thumbnailDataURI}
									alt="Agent thumbnail"
								/>
							{/if}
							<input
								aria-label="Set agent thumbnail"
								type="file"
								accept="image/*"
								on:change={setThumbnail}
							/>
						</div>
					</DetailViewSection>

					<DetailViewSection title="Base model">
						<GeneralDropdown
							aria-label="Base model"
							options={modelDropdownOptions}
							bind:chosenOption={chosenModel}
							placeholder="Choose base model..."
						/>
					</DetailViewSection>

					<DetailViewSection title="System prompt">
						<Textarea
							aria-label="System prompt"
							bind:value={
								modifiedAgent.systemPrompt
							}
						/>
					</DetailViewSection>

					<DetailViewSection title="Model parameters">
						<ParameterSlider
							label="Temperature"
							aria-label="Temperature"
							fallback={1.0}
							min={0.0}
							max={2.0}
							bind:value={
								modifiedAgent.modelParameters
									.temperature
							}
						/>
						<ParameterSlider
							label="Top K"
							aria-label="Top K"
							fallback={40}
							min={0}
							max={1000}
							bind:value={
								modifiedAgent.modelParameters
									.top_k
							}
						/>
					</DetailViewSection>

					<DetailViewSection title="Triggers">
						{#each triggers as trigger}
							<Toggle
								label={trigger[0].name}
								aria-label={trigger[0].name}
								bind:enabled={trigger[1]}
							/>
						{/each}
					</DetailViewSection>

					<DetailViewSection title="Actions">
						{#each actions as action}
							<Toggle
								label={action[0].displayName}
								aria-label={action[0]
									.displayName}
								bind:enabled={action[1]}
							/>
						{/each}
					</DetailViewSection>

					{#if id !== null}
						<DetailViewSection title="Delete agent">
							<DeleteButton
								aria-label="Delete agent"
								onclick={onDelete}
							/>
						</DetailViewSection>

						<DetailViewSection title="Save agent">
							<SaveButton
								aria-label="Save agent"
								onclick={onSave}
							/>
						</DetailViewSection>
					{:else}
						<DetailViewSection title="Create agent">
							<CreateButton
								aria-label="Create agent"
								onclick={onCreate}
							/>
						</DetailViewSection>
					{/if}
				</DetailView>
			</Loader>
		</Loader>
	</Loader>
</Loader>

