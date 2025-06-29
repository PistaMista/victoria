<script>
    import MonologueStatusIndicator from "$lib/components/indicators/MonologueStatusIndicator.svelte";
</script>

<div class="flex flex-row px-2 my-1 border-t-2 border-black hover:bg-slate-400">
    <div class="content-center">
        <MonologueStatusIndicator/>
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