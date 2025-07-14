<script lang="ts">
    import ChatOptionsView from "$lib/views/details/ChatOptionsView.svelte";
    import { page } from "$app/stores";
    
    $: id = Number($page.params.id)
</script>

<ChatOptionsView
    {id}
/>