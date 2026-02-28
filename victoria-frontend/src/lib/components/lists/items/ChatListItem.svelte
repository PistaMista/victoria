<script lang="ts">
	import type { Chat } from "$lib/types/chat";
	import { goto } from "$app/navigation";
	export let chat: Chat;

	function openChat() {
		goto(`/chats/${chat.id}`);
	}
</script>

<button
	on:click={openChat}
	class="flex flex-col px-2 my-1 border-t-2 border-black hover:bg-slate-400"
>
	<div class="font-bold">{chat.title}</div>
	<div>{chat.summary}</div>
</button>

