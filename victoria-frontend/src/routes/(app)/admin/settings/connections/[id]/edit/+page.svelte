<script lang="ts">
	import ConnectionDetailView from "$lib/views/details/ConnectionDetailView.svelte";
	import { page } from "$app/stores";

	$: id = Number($page.params.id);
</script>

<ConnectionDetailView {id} />

