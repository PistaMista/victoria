<script lang="ts">
    import ActionRepositoryDetailView from "$lib/views/details/ActionRepositoryDetailView.svelte";
    import { page } from "$app/stores";

    $: id = $page.params.id;
</script>

<ActionRepositoryDetailView
    {id}
/>