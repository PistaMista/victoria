<script lang="ts">
    import AgentDetailView from "$lib/views/details/AgentDetailView.svelte";
    import { page } from "$app/stores";

    $: id = $page.params.id;
</script>

<AgentDetailView
    {id}
/>