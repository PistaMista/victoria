<script lang="ts">
    import { afterUpdate } from "svelte";
    import AssistantMessage from "./ChatItem/Messages/AssistantMessage.svelte";
    import UserMessage from "./ChatItem/Messages/UserMessage.svelte";
    
    export let messages: Array<any> = [];
    
    let container: HTMLDivElement;

    // Scroll to the last message when the container element changes
    afterUpdate(() => {
        container.scrollTo(0, container.scrollHeight);
    })
    
    function delete_message(i: number) {
        messages = messages.toSpliced(i, 1);
    }
</script>

<div class="p-2 w-full h-full">
    <div class="p-2 h-full bg-gray-200 border border-slate-600 focus:border-primary-900 shadow-inner rounded-lg">
        <div bind:this={container} class="p-2 h-full overflow-y-auto scroll-smooth">
            {#each messages as message, i}
                {#if message.type == 'user'}
                    <UserMessage 
                        bind:content={message.content} 
                        delete_action={() => delete_message(i)}
                    />
                {:else}
                    <AssistantMessage 
                        bind:content={message.content}
                        delete_action={() => delete_message(i)}
                    />
                {/if}
            {/each}
        </div>
    </div>
</div>