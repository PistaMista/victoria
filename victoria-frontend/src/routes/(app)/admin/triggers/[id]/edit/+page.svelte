<script lang="ts">
    import TriggerDetailView from "$lib/views/details/TriggerDetailView.svelte";
    import { page } from "$app/stores";
    
    $: id = Number($page.params.id)
</script>

<TriggerDetailView
    {id}
/>