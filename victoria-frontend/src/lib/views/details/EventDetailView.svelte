<script>
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import DetailView from "$lib/views/DetailView.svelte";
</script>

<DetailView>
    <DetailViewSection title="Trigger">
        Receive email
    </DetailViewSection>
    
    <DetailViewSection title="Content">
        An email was received
    </DetailViewSection>
</DetailView>