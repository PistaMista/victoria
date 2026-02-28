<script lang="ts">
	import ListViewHeaderButton from "$lib/components/buttons/ListViewHeaderButton.svelte";
	import ListViewHeaderDropdown, {
		type Option,
	} from "$lib/components/dropdowns/ListViewHeaderDropdown.svelte";
	import ChatListItem from "$lib/components/lists/items/ChatListItem.svelte";
	import ListViewHeaderSearchBar from "$lib/components/search/ListViewHeaderSearchBar.svelte";
	import ListView from "$lib/views/ListView.svelte";
	import Loader from "$lib/components/placeholders/Loader.svelte";
	import { PlusOutline } from "flowbite-svelte-icons";
	import {
		getCurrentUserChats,
		createNewChat,
		type SortMode,
		getChatReceivers,
	} from "$lib/api/chatting";
	import type { Chat } from "$lib/types/chat";
	import { goto } from "$app/navigation";
	import { onMount } from "svelte";

	let chats: Chat[] = [];
	let receivers: string[] = [];
	let sortByOption: Option | null;
	let receiverOption: Option | null;
	let searchQuery: string = "";
	let mounted = false;

	let initPromise: Promise<void> = Promise.resolve();
	let dataPromise: Promise<void> = Promise.resolve();
	let createPromise: Promise<void> = Promise.resolve();

	async function init() {
		receivers = await getChatReceivers();
	}

	async function openNewChat() {
		let { id } = await createNewChat();
		let stringId = id.toString();
		goto(`/chats/${stringId}`);
	}

	onMount(async () => {
		mounted = true;
		initPromise = init();
	});

	$: if (mounted) {
		dataPromise = (async () => {
			let receiver: string | null = receiverOption?.value;
			let query: string | null = searchQuery ? searchQuery : null;
			let sortBy: SortMode = sortByOption?.value ?? "recent";
			chats = await getCurrentUserChats(sortBy, receiver, query);
		})();
	}
</script>

<Loader
	promise={initPromise}
	pendingMessage="Initializing..."
	rejectMessage="Failed to initialize view."
>
	<Loader
		promise={createPromise}
		pendingMessage="Creating new chat..."
		rejectMessage="Failed to create new chat."
	>
		<ListView>
			<svelte:fragment slot="header">
				<ListViewHeaderSearchBar
					ontype={(val) => {
						searchQuery = val;
					}}
				/>
				<div class="mx-2 content-center flex flex-row">
					<!-- Sort by Recent/Longest/Important -->
					<ListViewHeaderDropdown
						title="Sort"
						aria-label="Sort by"
						options={[
							{
								displayName: "Recent",
								ariaLabel: "Recent",
								value: "recent",
							},
							{
								displayName: "Longest",
								ariaLabel: "Length",
								value: "length",
							},
							{
								displayName: "Importance",
								ariaLabel: "Importance",
								value: "importance",
							},
						]}
						bind:chosenOption={sortByOption}
					/>
					<!-- Filter by chat receiver -->
					<ListViewHeaderDropdown
						title="Receiver"
						aria-label="Filter by chat receiver"
						options={[
							{
								displayName: "any",
								ariaLabel: "any",
								value: null,
							},
							...receivers.map((name) => ({
								displayName: name,
								ariaLabel: name,
								value: name,
							})),
						]}
						bind:chosenOption={receiverOption}
					/>

					<ListViewHeaderButton
						onclick={() => {
							createPromise = openNewChat();
						}}
						aria-label="Create chat"
						><PlusOutline
							class="w-6 h-6"
						/></ListViewHeaderButton
					>
				</div>
			</svelte:fragment>

			<svelte:fragment slot="items">
				<Loader
					promise={dataPromise}
					pendingMessage="Loading chats..."
					rejectMessage="Failed to load chats."
				>
					{#each chats as chat}
						<ChatListItem {chat} />
					{/each}
				</Loader>
			</svelte:fragment>
		</ListView>
	</Loader>
</Loader>

