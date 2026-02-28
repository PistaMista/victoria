<script lang="ts">
	import AgentDetailView from "$lib/views/details/AgentDetailView.svelte";
	import { page } from "$app/stores";

	$: id = Number($page.params.id);
</script>

<AgentDetailView {id} />

