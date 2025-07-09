<script lang="ts">
    import { getAllModels } from "$lib/api/models";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import LanguageModelToggle from "$lib/components/toggles/LanguageModelToggle.svelte";
    import type { Model } from "$lib/types/model";
    import DetailView from "$lib/views/DetailView.svelte";
    import { onMount } from "svelte";
    
    let models: Model[] = [];
    
    onMount(async () => {
        models = await getAllModels();
    })
</script>

<DetailView backRoute="/admin/settings">
    <DetailViewSection title="Ollama models">
        {#each models as model}
            <LanguageModelToggle {model}/>
        {/each}
    </DetailViewSection>
</DetailView>