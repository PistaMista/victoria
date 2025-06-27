<script lang="ts">
    import { Textarea, Button, Range, Input, Label, Checkbox } from "flowbite-svelte";
    import { ClockOutline, RocketOutline, CheckOutline, CloseOutline, RocketSolid, BrainSolid, HammerSolid, ReplyAllSolid } from "flowbite-svelte-icons";
</script>

<div class="w-full h-full overflow-y-auto">
    <div class="flex flex-col content-center mx-2 md:m-auto md:max-w-96">
        <div class="my-2">
            <!-- This is a DetailViewSection -->
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
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Status</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <div class="flex flex-row">
                    <!-- This is a MonologueStatusIndicator -->
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
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Assigned agent</Label>
            <div class="bg-slate-400 rounded-md p-2">
                AGENT CARD HERE
            </div>
        </div>
        <div class="my-2">
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Thoughts</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <div class="relative flex flex-col px-2 py-2 space-y-12">
                    
                    <!-- Thoughts -->
                    <!-- These "thought cards" should be collapsible - the thoughts can be quite long -->
                    <div class="rounded-md z-20 bg-slate-200 p-2">
                        <RocketSolid class="float-left mr-2"/>
                        <!-- This will be a link to the detail of the event -->
                        <div class="w-full font-semibold">Monitor emails</div>
                        Email received: "Hello, this is John I would like to invite you to the XYZ conference on the 18th of June..."
                    </div>
                    <div class="rounded-md z-20 bg-slate-200 p-2">
                        <BrainSolid class="float-left mr-2"/>
                        I should add the event contained in the email to the calendar
                    </div>
                    <div class="rounded-md z-20 bg-slate-200 p-2">
                        <div class="flex flex-col space-y-2">
                            <div class="border-b-2 border-slate-500 w-full">
                                <HammerSolid class="float-left mr-2"/>
                                <div class="w-full font-semibold">
                                    Add to calendar
                                </div>
                                <ul>
                                    <li>description: Conference XYZ</li>
                                    <li>date: 2025-06-10</li>
                                    <li>time: 10:00 AM</li>
                                </ul>
                            </div>
                            <div class="w-full">
                                <ReplyAllSolid class="float-left mr-2"/>
                                Event successfully added to calendar./Exception thrown: SDNJANSJKDNKJN
                            </div>
                        </div>

                    </div>
                    <div class="rounded-md z-20 bg-slate-200 p-2">
                        <div class="flex flex-row content-center text-lime-600 justify-center">
                            <CheckOutline class="w-10 h-10 text-inherit"/>
                            <div class="content-center font-semibold text-inherit">SUCCESS</div>
                        </div>
                    </div>
                    <div class="rounded-md z-20 bg-slate-200 p-2">
                        <div class="flex flex-row content-center text-red-600 justify-center">
                            <CloseOutline class="w-10 h-10 text-inherit"/>
                            <div class="content-center font-semibold text-inherit">FAILURE</div>
                        </div>
                    </div>

                    <!-- Dotted line for decoration-->
                    <div class="absolute z-10 top-0 bottom-4 left-6 w-0.5 border-l-4 border-dotted border-gray-200"/>
                </div>
            </div>
        </div>
        <div class="my-2">
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Abort monologue</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <Button class="w-full font-bold bg-red-600"><CloseOutline/>ABORT</Button>
            </div>
        </div>
    </div>
</div>