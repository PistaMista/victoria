<script lang="ts">
    import { marked } from 'marked';
    import ChatItemBase from '../ChatItemBase.svelte';
    import ContextMenuBase from '../ContextMenuBase.svelte';
    import { EditOutline, TrashBinOutline } from 'flowbite-svelte-icons';
    import { Textarea } from 'flowbite-svelte';

    export let content = "";
    export let delete_action: () => void;
    let edit_mode = false;
</script>

<ChatItemBase justify_end={true} inner_class="bg-primary-900">
    <svelte:fragment slot="content">
        {#if !edit_mode}
            <!-- FIXME: There is totally an XSS attack here -->
            <div role="article">
                {@html marked(content)}
            </div>
        {:else}
            <Textarea
                class="rounded-lg"
                bind:value={content}
                on:blur={() => { edit_mode = false; }}
                autofocus
            />
        {/if}
    </svelte:fragment>
    
    <svelte:fragment slot="menu">
        <ContextMenuBase
            context_actions={[
                {
                    icon_component: EditOutline,
                    action: () => { edit_mode = !edit_mode; }
                },
                {
                    icon_component: TrashBinOutline,
                    action: delete_action
                }
            ]}
        />
    </svelte:fragment>
</ChatItemBase>