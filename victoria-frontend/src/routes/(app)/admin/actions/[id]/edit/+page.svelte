<script lang="ts">
	import ActionRepositoryDetailView from "$lib/views/details/ActionRepositoryDetailView.svelte";
	import { page } from "$app/stores";

	$: id = Number($page.params.id);
</script>

<ActionRepositoryDetailView {id} />

