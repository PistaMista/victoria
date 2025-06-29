<script lang="ts">
    import AgentStatusIndicator from "../indicators/AgentStatusIndicator.svelte";
    import MonologueMiniCard from "./MonologueMiniCard.svelte";
    import { DotsVerticalOutline } from "flowbite-svelte-icons";
</script>

<div class="bg-slate-300 rounded-md p-2 flex flex-col md:w-72 m-1">
    <div class="flex flex-row content-center pl-1 mb-1">
        <div class="font-bold">
            Researcher
        </div>
        <div class="grow"/>
        <AgentStatusIndicator/>
        <div>
            <DotsVerticalOutline/>
        </div>
    </div>
    <div class="flex flex-row">
        <div class="bg-orange-200 rounded-md h-14 w-14 p-1"></div>
        <div class="grow h-24 bg-slate-400 rounded-md ml-1 p-1 overflow-y-scroll">
            <div class="flex flex-col">
                <MonologueMiniCard/>
                <MonologueMiniCard/>
                <MonologueMiniCard/>
            </div>
        </div>
    </div>
</div>