<script lang="ts">
    import type { ActionConfirmationContent } from "$lib/types/message";
    import { Button, ButtonGroup } from "flowbite-svelte";
    import { ExclamationCircleSolid, CheckOutline, CloseOutline } from "flowbite-svelte-icons";
    import ActionContent from "$lib/components/monologue/thoughts/ActionContent.svelte";
    import { onMount } from "svelte";
    import { getQueryAnswer, sendQueryAnswer } from "$lib/api/queries";
    import Loader from "$lib/components/placeholders/Loader.svelte";
    
    export let content: ActionConfirmationContent;

    let answer: boolean | null = null;
    
    let sendAnswerPromise: Promise<any> = Promise.resolve();
    let loadAnswerPromise: Promise<any> = Promise.resolve();

    async function loadAnswer () {
        answer = await getQueryAnswer(content.queryId);
    }
    
    async function sendAnswer(answer: boolean) {
        await sendQueryAnswer(content.queryId, answer);
        loadAnswerPromise = loadAnswer();
    }

    function execute() {
        sendAnswerPromise = sendAnswer(true);
    }
    
    function abort() {
        sendAnswerPromise = sendAnswer(false);
    }
    
    onMount(() => {
        loadAnswerPromise = loadAnswer();
    })
</script>

<div class="flex flex-col">
    <div class="bg-gradient-to-tr from-red-500 to-orange-500 justify-center flex flex-row font-semibold rounded-md">
        <ExclamationCircleSolid class="mt-0.5 mr-2"/>
        ACTION CONFIRMATION REQUEST
        <ExclamationCircleSolid class="mt-0.5 ml-2"/>
    </div>
    <div class="bg-slate-400 rounded-md my-2 p-2">
        <ActionContent content={content.invocationThought}/>
    </div>
    
    <Loader
        promise={loadAnswerPromise}
        pendingMessage="Loading existing answer..."
        rejectMessage="Failed to load existing answer"
    >
    <Loader
        promise={sendAnswerPromise}
        pendingMessage="Sending answer..."
        rejectMessage="Failed to send answer"
    >
        {#if answer === null}
            <ButtonGroup class="my-1">
                <Button 
                    class="bg-lime-500 grow"
                    aria-label="Execute action"
                    on:click={execute}
                ><CheckOutline/>EXECUTE</Button>
                <Button 
                    class="bg-red-500 grow"
                    aria-label="Abort action"
                    on:click={abort}
                ><CloseOutline/>ABORT</Button>
            </ButtonGroup>
        {:else if answer === true}
            <div class="font-bold text-lime-500">
                <CheckOutline/>
                CONFIRMED
            </div>
        {:else if answer === false}
            <div class="font-bold text-red-500">
                <CloseOutline/>
                ABORTED
            </div>
        {/if}
    </Loader>
    </Loader>
</div>