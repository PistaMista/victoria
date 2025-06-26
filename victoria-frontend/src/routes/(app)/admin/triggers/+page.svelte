<script>
    import Button from "$lib/components/button/Button.svelte";
    import { Search } from "flowbite-svelte";   
    import { ChevronLeftOutline, PlusOutline } from "flowbite-svelte-icons";
</script>

<div class="flex flex-col w-full h-full">
    <div class="p-1 bg-slate-400 flex flex-row">
        <!-- This is a back button -->
        <div class="flex flex-row hover:bg-slate-500 rounded-md p-1">
            <ChevronLeftOutline class="h-8 w-8 my-auto"/>
            <div class="content-center mr-2">
                Back
            </div>
        </div>
        <Search class="grow max-h-10 mb-1 md:mb-0"></Search>
        <div class="hover:bg-slate-300 p-1 rounded-md">
            <Button class="flex flex-row text-nowrap"><PlusOutline class="w-6 h-8 my-auto"/></Button>
        </div>
    </div>
    
    <div class="flex flex-col grow min-h-0 bg-slate-300 overflow-y-scroll">
        <!-- This is a TriggerListItem? -->
        <div class="flex flex-col px-2 my-1 border-t-2 border-black hover:bg-slate-400">
            <div class="flex flex-row">
                <div class="font-bold">
                    Collect news
                </div>
                <div class="ml-auto font-bold">
                    POLL
                </div>
            </div>
            <div>
                URL: https://linuxjournal.com/rss
            </div>
        </div>

        <div class="flex flex-col px-2 my-1 border-t-2 border-black hover:bg-slate-400">
            <div class="flex flex-row">
                <div class="font-bold">
                    Discord message arrived
                </div>
                <div class="ml-auto font-bold">
                    WEBHOOK
                </div>
            </div>
            <div>
                URL: /hooks/danwkjdnkjnjj
            </div>
        </div>

        <div class="flex flex-col px-2 my-1 border-t-2 border-black hover:bg-slate-400">
            <div class="flex flex-row">
                <div class="font-bold">
                    General chat
                </div>
                <div class="ml-auto font-bold">
                    CHAT
                </div>
            </div>
            <div>
                Name: General
            </div>
        </div>

        <div class="flex flex-col px-2 my-1 border-t-2 border-black hover:bg-slate-400">
            <div class="flex flex-row">
                <div class="font-bold">
                    Check logs
                </div>
                <div class="ml-auto font-bold">
                    TIMER
                </div>
            </div>
            <div>
                Every day at 20:00
            </div>
        </div>
    </div>
</div>