<script>
    import { Label } from "flowbite-svelte";
    import { HammerSolid, CogSolid, RocketSolid, UserSolid, ChevronRightOutline } from "flowbite-svelte-icons";
</script>

<!-- COMPONENT: AdminDetailView -->
<!-- COMPONENT: DetailView -->
<div class="w-full h-full overflow-y-auto">
    <div class="flex flex-col content-center mx-2 md:m-auto md:max-w-96">
        <div class="my-2">
            <!-- COMPONENT: DetailViewSection -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Administration options</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <div class="flex flex-col space-y-2">
                    <!-- COMPONENT: OptionsRouteButton -->
                    <div class="flex flex-row w-full hover:bg-slate-500 p-1 rounded-md">
                        <div class="rounded-full bg-black p-1">
                            <HammerSolid class="w-6 h-6 text-orange-500"/>
                        </div>
                        <div class="ml-2 content-center">
                            Actions
                        </div>
                        <ChevronRightOutline class="h-8 w-8 my-auto ml-auto"/>
                    </div>

                    <!-- COMPONENT: OptionsRouteButton -->
                    <div class="flex flex-row w-full hover:bg-slate-500 p-1 rounded-md">
                        <div class="rounded-full bg-black p-1">
                            <RocketSolid class="w-6 h-6 text-purple-500"/>
                        </div>
                        <div class="ml-2 content-center">
                            Triggers
                        </div>
                        <ChevronRightOutline class="h-8 w-8 my-auto ml-auto"/>
                    </div>

                    <!-- COMPONENT: OptionsRouteButton -->
                    <div class="flex flex-row w-full hover:bg-slate-500 p-1 rounded-md">
                        <div class="rounded-full bg-black p-1">
                            <UserSolid class="w-6 h-6 text-white"/>
                        </div>
                        <div class="ml-2 content-center">
                            Users
                        </div>
                        <ChevronRightOutline class="h-8 w-8 my-auto ml-auto"/>
                    </div>

                    <!-- COMPONENT: OptionsRouteButton -->
                    <div class="flex flex-row w-full hover:bg-slate-500 p-1 rounded-md">
                        <div class="rounded-full bg-black p-1">
                            <CogSolid class="w-6 h-6 text-blue-500"/>
                        </div>
                        <div class="ml-2 content-center">
                            Settings
                        </div>
                        <ChevronRightOutline class="h-8 w-8 my-auto ml-auto"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>