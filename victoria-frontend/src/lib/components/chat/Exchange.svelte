<script lang="ts">
    import Message from "./Message.svelte";
    import MonologueStatusIndicator from "../indicators/MonologueStatusIndicator.svelte";
    import { EditOutline, RefreshOutline, ChevronLeftOutline, ChevronRightOutline } from "flowbite-svelte-icons";
</script>

<div class="w-full flex flex-col">
    <!-- This is the user's Message -->
    <div class="border-b-2 border-slate-500 bg-orange-200 rounded-t-md p-1">
        <Message/>
    </div>
    <!-- These are the Message(s) sent by the Agent -->
    <div class="flex flex-col space-y-2 border-b-2 border-slate-500 border-dashed bg-slate-100 p-1">
        <Message/>
        <Message/>
        <Message/>
    </div>
    <!-- Running monologue info -->
    <div class="flex flex-row mt-1">
        <a class="font-semibold hover:text-blue-500" href="/monologues/2">Answer user query</a>
        <div class="ml-auto">
            <MonologueStatusIndicator/>
        </div>
    </div>
    <!-- These buttons are only shown if there is no Exchange at this level with a non-completed Monologue -->
    <div class="flex flex-row mt-1 space-x-1 content-center">
        <EditOutline class="rounded-md hover:bg-slate-500"/>
        <RefreshOutline class="rounded-md hover:bg-slate-500"/>
        <div class="grow"/>
        <ChevronLeftOutline class="rounded-md hover:bg-slate-500"/>
        <div class="font-medium">
            1/1
        </div>
        <ChevronRightOutline class="rounded-md hover:bg-slate-500"/>
    </div>
</div>