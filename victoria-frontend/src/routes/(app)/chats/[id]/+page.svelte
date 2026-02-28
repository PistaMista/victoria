<script lang="ts">
	import ChatView from "$lib/views/ChatView.svelte";
	import { page } from "$app/stores";

	$: id = Number($page.params.id);
</script>

<ChatView {id} />

