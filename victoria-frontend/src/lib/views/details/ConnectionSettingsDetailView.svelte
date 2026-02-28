<script>
	import ConnectionsList from "$lib/components/lists/ConnectionsList.svelte";
	import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
	import DetailView from "$lib/views/DetailView.svelte";
</script>

<DetailView backRoute="/admin/settings">
	<DetailViewSection title="Ollama">
		<ConnectionsList />
	</DetailViewSection>
</DetailView>

