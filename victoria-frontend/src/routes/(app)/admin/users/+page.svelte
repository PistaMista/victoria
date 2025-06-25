<script>
    import { Label, Button } from "flowbite-svelte";
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
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Registered users</Label>
            <div class="bg-slate-400 rounded-md p-2">
                <div class="flex flex-col space-y-2">
                    <div class="flex flex-row">
                        <Button class="ml-auto w-6 h-6 p-0"><PlusOutline/></Button>
                    </div>
                    
                    <!-- This is the list of users -->
                    <div class="flex flex-col">
                        <!-- This is a list item representing the user -->
                        <div class="flex flex-row">
                            <!-- This is a UserAvatar -->
                            <div class="rounded-full w-6 h-6 bg-orange-500 mr-1"></div>
                            <div class="mr-auto">Kryštof Albrecht</div>
                            <div class="rounded-md bg-blue-500 px-1 mr-1 font-bold text-white">ADMIN</div>
                            <Button class="w-6 h-6 p-0"><CogSolid/></Button>
                        </div>                        
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>