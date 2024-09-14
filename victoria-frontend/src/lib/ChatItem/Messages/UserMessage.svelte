<script lang="ts">
    import { marked } from 'marked';
    import ChatItemBase from '../ChatItemBase.svelte';
    import ContextMenuBase from '../ContextMenuBase.svelte';
    export let content = "";
</script>

<ChatItemBase justify_end={true} inner_class="bg-primary-900">
    <svelte:fragment slot="content">
        <!-- FIXME: There is totally an XSS attack here -->
        {@html marked(content)}
    </svelte:fragment>
    
    <svelte:fragment slot="menu">
        <ContextMenuBase/>
    </svelte:fragment>
</ChatItemBase>