<script lang="ts">
    import { getAllModels } from "$lib/api/models";
    import Loader from "$lib/components/placeholders/Loader.svelte";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import LanguageModelToggle from "$lib/components/toggles/LanguageModelToggle.svelte";
    import type { Model } from "$lib/types/model";
    import DetailView from "$lib/views/DetailView.svelte";
    import { onMount } from "svelte";
    
    let models: Model[] = [];
    
    let dataPromise: Promise<any> = Promise.resolve();
    
    async function load() {
        models = await getAllModels();
    }
    
    onMount(() => {
        dataPromise = load();
    })
</script>

<DetailView backRoute="/admin/settings">
    <DetailViewSection title="Ollama models">
        <Loader
            promise={dataPromise}
            pendingMessage="Loading models..."
            rejectMessage="Failed to load models"
        >
            {#each models as model}
                <LanguageModelToggle {model}/>
            {/each}
        </Loader>
    </DetailViewSection>
</DetailView>