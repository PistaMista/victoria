<script lang="ts">
    import { ButtonGroup, Button, Textarea } from "flowbite-svelte";
    import { PaperPlaneSolid, HammerSolid } from "flowbite-svelte-icons";
    import { goto } from "$app/navigation";
    import { sendMessageToChat } from "$lib/api/chatting";
    import Loader from "../placeholders/Loader.svelte";
    
    export let id: number;
    
    let message: string = "";
    
    let messagePromise: Promise<any> = Promise.resolve();
    
    function openChatOptions() {
        goto(`/chats/${id}/options`);       
    }
    
    function sendMessage() {
        if (message.length > 0) {
            messagePromise = sendMessageToChat(id, message);
        }
    }
</script>

<Loader
    promise={messagePromise}
    pendingMessage="Sending message..."
    rejectMessage="Failed to send message"
>
<ButtonGroup class="md:bg-slate-400 p-0 md:p-2 md:w-2/3 md:m-auto rounded-none md:rounded-md">
    <Button 
        aria-label="Show chat options"
        class="w-8 min-h-0" 
        on:click={openChatOptions}
    ><HammerSolid/></Button>
    <Textarea 
        aria-label="Message box"
        class="bg-slate-200 border-none rounded-none"
        bind:value={message}
    />
    <Button 
        aria-label="Send message"
        class="w-12 min-h-0"
        on:click={sendMessage}
    ><PaperPlaneSolid/></Button>
</ButtonGroup>
</Loader>