<script>
    import { ButtonGroup, Textarea, Button } from "flowbite-svelte";
    import { PaperPlaneSolid, PaperClipOutline, HammerSolid, CloseOutline, CheckOutline, ExclamationCircleSolid, RefreshOutline, EditSolid, ChevronLeftOutline, ChevronRightOutline, EditOutline } from "flowbite-svelte-icons";
</script>

<div class="w-full h-full flex flex-col pt-2 md:pb-2">
    <!-- COMPONENT: ChatWindow -->
    <div class="grow min-h-0 mb-2 overflow-y-scroll">
        <div class="flex flex-col md:w-2/3 mx-2 md:m-auto">
            <!-- COMPONENT: Exchange -->
            <div class="w-full flex flex-col">
                <!-- This is the user's Message -->
                <div class="border-b-2 border-slate-500 bg-orange-200 rounded-t-md p-1">
                    <!-- COMPONENT: Message -->
                    <div class="flex flex-col">
                        <div class="flex flex-row">
                            <!-- This is the name of the actor -->
                            <div class="font-semibold mr-auto">Krystof</div>
                            <!-- This is a DateDisplay -->
                            <div class="text-gray-600 text-xs content-center">Today at 10:00 AM</div>                            
                        </div>
                        <!-- The content of the Message varies by its type -->
                        <!-- There will be different Content components, see agent messages for all types -->
                        <div class="prose">Lorem askjdnkja nsjkdn akjns jknasjkd njkasnd jknasjkdn jkansj kdnkajsnd</div>
                    </div>
                </div>
                <!-- These are the Message(s) sent by the Agent -->
                <div class="flex flex-col space-y-2 border-b-2 border-slate-500 border-dashed bg-slate-100 p-1">
                    <!-- COMPONENT: Message -->
                    <div class="flex flex-col">
                        <div class="flex flex-row">
                            <div class="font-semibold mr-auto">Researcher</div>
                            <div class="text-gray-600 text-xs content-center">Today at 10:01 AM</div>                            
                        </div>
                        <!-- COMPONENT: MarkdownContent -->
                        <div class="prose">I have found XYZ</div>
                    </div>
                    <!-- COMPONENT: Message -->
                    <div class="flex flex-col">
                        <div class="flex flex-row">
                            <div class="font-semibold mr-auto">Researcher</div>
                            <div class="text-gray-600 text-xs content-center">Today at 10:01 AM</div>                            
                        </div>
                        <!-- COMPONENT: ImageContent -->
                        <div class="w-2/3 mx-auto h-24 bg-red-500 rounded-md"/>
                    </div>
                    <!-- COMPONENT: Message -->
                    <div class="flex flex-col">
                        <div class="flex flex-row">
                            <div class="font-semibold mr-auto">Researcher</div>
                            <div class="text-gray-600 text-xs content-center">Today at 10:01 AM</div>                            
                        </div>
                        <!-- COMPONENT: ActionConfirmationContent -->
                        <div class="flex flex-col">
                            <div class="bg-gradient-to-tr from-red-500 to-orange-500 justify-center flex flex-row font-semibold rounded-md">
                                <ExclamationCircleSolid class="mt-0.5 mr-2"/>
                                ACTION CONFIRMATION REQUEST
                                <ExclamationCircleSolid class="mt-0.5 ml-2"/>
                            </div>
                            <div class="bg-slate-400 rounded-md my-2 p-2">
                                <div class="w-full font-semibold">
                                    Web search
                                </div>
                                <ul>
                                    <li>query: "distance to the moon"</li>
                                </ul>
                            </div>
                            <ButtonGroup class="my-1">
                                <Button class="bg-lime-500 grow"><CheckOutline/>EXECUTE</Button>
                                <Button class="bg-red-500 grow"><CloseOutline/>ABORT</Button>
                            </ButtonGroup>
                        </div>
                    </div>
                    <!-- COMPONENT: Message -->
                    <div class="flex flex-col">
                        <div class="flex flex-row">
                            <div class="font-semibold mr-auto">Researcher</div>
                            <div class="text-gray-600 text-xs content-center">Today at 10:01 AM</div>                            
                        </div>

                        <!-- COMPONENT: ChoicePromptContent -->
                        <div class="flex flex-col">
                            <div class="bg-gradient-to-tr from-red-500 to-orange-500 justify-center flex flex-row font-semibold rounded-md">
                                <ExclamationCircleSolid class="mt-0.5 mr-2"/>
                                CHOICE REQUIRED
                                <ExclamationCircleSolid class="mt-0.5 ml-2"/>
                            </div>
                            <div class="text-center">
                                Please choose an account to sign into
                            </div>

                            <div class="flex flex-col space-y-2 rounded-md p-2 m-1 bg-slate-500">
                                <Button class="w-full">This one</Button>
                                <Button class="w-full">That one</Button>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- <div>Running monologue info</div> -->
                <!-- COMPONENT: MonologueStatusIndicator -->
                <div class="flex flex-row mt-1">
                    <a class="font-semibold hover:text-blue-500" href="/monologues/2">Answer user query</a>
                    <div class="bg-black rounded-md px-1 font-bold text-lime-500 ml-auto">RUNNING</div>
                </div>
                <!-- These buttons are only shown if there is no Exchange at this level with a non-completed Monologue -->
                <!-- COMPONENT: ExchangeContextButtons? -->
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
        </div>
    </div>
    
    <!-- COMPONENT: ChatPrompt -->
    <ButtonGroup class="md:bg-slate-400 p-0 md:p-2 md:w-2/3 md:m-auto rounded-none md:rounded-md">
        <Button class="w-8 min-h-0"><HammerSolid/></Button>
        <Button class="w-8 min-h-0"><PaperClipOutline/></Button>
        <Textarea class="bg-slate-200 border-none rounded-none"/>
        <Button class="w-12 min-h-0"><PaperPlaneSolid/></Button>
    </ButtonGroup>
</div>