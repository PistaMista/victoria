<script lang="ts">
	import EventDetailView from "$lib/views/details/EventDetailView.svelte";
	import { page } from "$app/stores";

	$: id = Number($page.params.id);
</script>

<EventDetailView {id} />

