<script lang="ts">
    import MonologueDetailView from "$lib/views/details/MonologueDetailView.svelte";
    import { page } from "$app/stores";

    $: id = $page.params.id;
</script>

<MonologueDetailView
    id={Number(id)}
/>