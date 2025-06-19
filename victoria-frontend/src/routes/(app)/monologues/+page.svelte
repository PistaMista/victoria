<script lang="ts">
    import { Search } from "flowbite-svelte";   
</script>

<div class="flex flex-col w-full h-full">
    <div class="p-1 bg-slate-400 flex flex-row">
        <Search class="grow max-h-8 md:max-w-72"></Search>
        <div class="mx-2 content-center">
            FILTERS
        </div>
    </div>
    
    <div class="flex flex-col grow min-h-0 bg-slate-300 overflow-y-scroll">
        <div class="flex flex-row px-2 my-1 border-t-2 border-black hover:bg-slate-400">
            <div class="content-center">
                <div class="flex flex-col">
                    <div class="font-bold text-lime-600 rounded-md bg-slate-600 p-1">
                        RUNNING
                    </div>
                    <div class="text-center">
                        20m39s
                    </div>
                </div>
            </div>
            <div class="grow mx-2 min-w-0 flex flex-col">
                <div class="font-bold">
                    Research thesis ideas
                </div>
                <div>
                    Searching the web for sources...
                </div>

                <div>
                    Started by <span class="font-semibold text-blue-500">Researcher</span> (<span class="font-semibold text-orange-400">Timer</span>) 20m ago
                </div>
            </div>
        </div>
    </div>
</div>