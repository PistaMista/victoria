<script>
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import LanguageModelToggle from "$lib/components/toggles/LanguageModelToggle.svelte";
    import DetailView from "$lib/views/DetailView.svelte";
</script>

<DetailView backRoute="/admin/settings">
    <DetailViewSection title="Ollama models">
        <LanguageModelToggle/>
    </DetailViewSection>
</DetailView>