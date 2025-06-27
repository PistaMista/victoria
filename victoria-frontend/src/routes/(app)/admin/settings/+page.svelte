<script>
    import { Label } from "flowbite-svelte";
    import { LinkOutline, CogSolid, BrainSolid, ChevronRightOutline, ChevronLeftOutline } from "flowbite-svelte-icons";
</script>

<!-- COMPONENT: SettingsDetailView -->
<!-- COMPONENT: DetailView -->
<div class="w-full h-full overflow-y-auto">
    <div class="hidden md:inline float-left">
        <!-- COMPONENT: BackButton -->
        <div class="flex flex-row hover:bg-slate-500 rounded-md p-1">
            <ChevronLeftOutline class="h-8 w-8 my-auto"/>
            <div class="content-center mr-2">
                Back
            </div>
        </div>
    </div>

    <div class="flex flex-col content-center mx-2 md:m-auto md:max-w-96">
        <div class="md:hidden">
            <!-- COMPONENT: BackButton -->
            <div class="flex flex-row hover:bg-slate-500 rounded-md p-1">
                <ChevronLeftOutline class="h-8 w-8 my-auto"/>
                <div class="content-center mr-2">
                    Back
                </div>
            </div>
        </div>            

        <div class="my-2">
            <!-- COMPONENT: DetailViewSection -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Settings</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <div class="flex flex-col space-y-2">
                    <!-- COMPONENT: OptionsRouteButton -->
                    <div class="flex flex-row w-full hover:bg-slate-500 p-1 rounded-md">
                        <div class="rounded-full bg-black p-1">
                            <CogSolid class="w-6 h-6 text-orange-500"/>
                        </div>
                        <div class="ml-2 content-center">
                            General
                        </div>
                        <ChevronRightOutline class="h-8 w-8 my-auto ml-auto"/>
                    </div>

                    <!-- COMPONENT: OptionsRouteButton -->
                    <div class="flex flex-row w-full hover:bg-slate-500 p-1 rounded-md">
                        <div class="rounded-full bg-black p-1">
                            <LinkOutline class="w-6 h-6 text-purple-500"/>
                        </div>
                        <div class="ml-2 content-center">
                            Connections
                        </div>
                        <ChevronRightOutline class="h-8 w-8 my-auto ml-auto"/>
                    </div>

                    <!-- COMPONENT: OptionsRouteButton -->
                    <div class="flex flex-row w-full hover:bg-slate-500 p-1 rounded-md">
                        <div class="rounded-full bg-black p-1">
                            <BrainSolid class="w-6 h-6 text-white"/>
                        </div>
                        <div class="ml-2 content-center">
                            Models
                        </div>
                        <ChevronRightOutline class="h-8 w-8 my-auto ml-auto"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>