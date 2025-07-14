<script lang="ts">
    import UserDetailView from "$lib/views/details/UserDetailView.svelte";
    import { page } from "$app/stores";
    
    $: id = Number($page.params.id)
</script>

<UserDetailView
    {id}
/>