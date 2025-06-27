<script>
    import { Label, Button, Checkbox, Input } from "flowbite-svelte";
    import {  ChevronLeftOutline, PlusOutline, TrashBinSolid, CogSolid } from "flowbite-svelte-icons";
</script>

<!-- TODO: Decide how to abstract the general layout of these settings menus into a Component - the back button and such -->
<div class="w-full h-full overflow-y-auto">
    <div class="hidden md:inline float-left">
        <!-- This is a back button -->
        <div class="flex flex-row hover:bg-slate-500 rounded-md p-1">
            <ChevronLeftOutline class="h-8 w-8 my-auto"/>
            <div class="content-center mr-2">
                Back
            </div>
        </div>
    </div>

    <div class="flex flex-col content-center mx-2 md:m-auto md:max-w-96">
        <div class="md:hidden">
            <!-- This is a back button -->
            <div class="flex flex-row hover:bg-slate-500 rounded-md p-1">
                <ChevronLeftOutline class="h-8 w-8 my-auto"/>
                <div class="content-center mr-2">
                    Back
                </div>
            </div>
        </div>            

        <div class="my-2">
            <!-- This is a DetailViewSection -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Username</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <div class="flex flex-col space-y-2">
                    <Input/>
                </div>
            </div>
        </div>

        <div class="my-2">
            <!-- This is a DetailViewSection -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">New password</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <div class="flexactions flex-col space-y-2">
                    <Input/>
                </div>
            </div>
        </div>

        <div class="my-2">
            <!-- This is a DetailViewSection -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Enable admin role</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <Checkbox/>
            </div>
        </div>
        

        <div class="my-2">
            <!-- This is a DetailViewSection -->
            <!-- This section is the same as the chat options view and permitted actions view for users -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Permitted agent actions</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <div class="flex flex-col space-y-2">
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Send chat message
                        </div>
                        <Checkbox/>
                    </div>
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Search web
                        </div>
                        <Checkbox/>
                    </div>
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Access task list
                        </div>
                        <Checkbox/>
                    </div>
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Access Zettelkasten
                        </div>
                        <Checkbox/>
                    </div>
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Use memory
                        </div>
                        <Checkbox/>
                    </div>
                </div>
            </div>
        </div>

        <div class="my-2">
            <!-- This is a DetailViewSection -->
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Permitted agent triggers</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <div class="flex flex-col space-y-2">
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Chat
                        </div>
                        <Checkbox/>
                    </div>
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Timer
                        </div>
                        <Checkbox/>
                    </div>
                    <div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
                        <div class="font-bold grow">
                            Task passing due date
                        </div>
                        <Checkbox/>
                    </div>
                </div>
            </div>
        </div>

        <Button class="w-full bg-red-500">DELETE USER</Button>
        
        <Button class="font-bold">SAVE USER</Button>
    </div>
</div>