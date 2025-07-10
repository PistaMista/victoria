<script lang="ts">
    import Loader from "./Loader.svelte";
</script>

<Loader
    pendingMessage= "Loading items..."
    rejectMessage= "Failed to load items"
    promise={new Promise((resolve, reject) => { resolve() })} 
>
    CHILD
</Loader>