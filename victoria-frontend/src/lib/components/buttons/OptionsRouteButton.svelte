<script lang="ts">
    import { CogSolid, ChevronRightOutline } from "flowbite-svelte-icons";
    import type { ComponentType } from "svelte";
    export let icon: ComponentType;
    export let text: String;
</script>

<div class="flex flex-row w-full hover:bg-slate-500 p-1 rounded-md">
    <div class="rounded-full bg-black p-1">
        <svelte:component this={icon} class="w-6 h-6 text-white"/>
    </div>
    <div class="ml-2 content-center">
        {text}
    </div>
    <ChevronRightOutline class="h-8 w-8 my-auto ml-auto"/>
</div>