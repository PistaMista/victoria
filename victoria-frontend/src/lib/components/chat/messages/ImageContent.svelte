<script lang="ts">
    import type { ImageContent } from "$lib/types/message";

    export let content: ImageContent;
</script>

<img src={content.imageDataURI} class="w-2/3 mx-auto h-24 bg-red-500 rounded-md"/>