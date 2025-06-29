<script lang="ts">
    import { Textarea, Button, Range, Input, Label, Checkbox } from "flowbite-svelte";
    import { ClockOutline, RocketOutline, CheckOutline, CloseOutline, RocketSolid, BrainSolid, HammerSolid, ReplyAllSolid } from "flowbite-svelte-icons";
    import AbortButton from "$lib/components/buttons/AbortButton.svelte";
    import FailureContent from "$lib/components/monologue/thoughts/FailureContent.svelte";
    import SuccessContent from "$lib/components/monologue/thoughts/SuccessContent.svelte";
    import ActionContent from "$lib/components/monologue/thoughts/ActionContent.svelte";
    import VerbatimContent from "$lib/components/monologue/thoughts/VerbatimContent.svelte";
    import TriggerContent from "$lib/components/monologue/thoughts/TriggerContent.svelte";
    import Thought from "$lib/components/monologue/Thought.svelte";
    import ThoughtTimeline from "$lib/components/monologue/ThoughtTimeline.svelte";
</script>

<!-- COMPONENT: MonologueDetailView -->
<!-- COMPONENT: DetailView -->
<div class="w-full h-full overflow-y-auto">
    <div class="flex flex-col content-center mx-2 md:m-auto md:max-w-96">
        <div class="my-2">
            <!-- COMPONENT: DetailViewSection -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Summary</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <div class="border-b-2 font-semibold">
                    Research thesis ideas
                </div>
                <div>
                    Searching for sources on the web
                </div>
            </div>
        </div>
        <div class="my-2">
            <!-- COMPONENT: DetailViewSection -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Status</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <div class="flex flex-row">
                    <!-- COMPONENT: MonologueStatusIndicator -->
                    <div class="bg-black rounded-md px-1 font-bold text-lime-500">RUNNING</div>
                    <div class="grow"/>
                    <div class="mx-1 flex flex-row">
                        <ClockOutline/>
                        20m39s
                    </div>
                    <div class="px-1 border-l-2 flex flex-row">
                        <RocketOutline/>
                        20m
                    </div>
                    <div class="px-1 border-l-2 flex flex-row">
                        <CheckOutline/>
                        20m
                    </div>
                </div>
            </div>
        </div>
        <div class="my-2">
            <!-- COMPONENT: DetailViewSection -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Assigned agent</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <!-- COMPONENT: AgentCard -->
                AGENT CARD HERE
            </div>
        </div>
        <div class="my-2">
            <!-- COMPONENT: DetailViewSection -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Thoughts</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <ThoughtTimeline/>
            </div>
        </div>
        
        <!-- COMPONENT: DetailViewSection -->
        <div class="my-2">
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Abort monologue</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <AbortButton/>
            </div>
        </div>
    </div>
</div>