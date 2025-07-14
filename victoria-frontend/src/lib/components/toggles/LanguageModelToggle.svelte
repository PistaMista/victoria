<script lang="ts">
    import { setModelEnabled } from "$lib/api/models";
    import type { Model } from "$lib/types/model";
    import { Checkbox } from "flowbite-svelte";
    import Loader from "../placeholders/Loader.svelte";
    
    export let model: Model;
    
    let enablePromise: Promise<any> = Promise.resolve();
    
    function onCheckboxChange() {
        enablePromise = setModelEnabled(model.id, model.enabled);
    }
</script>

<div class="flex flex-row bg-slate-500 rounded-md p-1">
    <Loader
        promise={enablePromise}
        pendingMessage={model.enabled ? "Disabling model..." : "Enabling model..."}
        rejectMessage={model.enabled ? "Failed to disable model" : "Failed to enable model"}
    >
        <div class="text-white mr-auto">
            {model.name}
        </div>
        <Checkbox bind:checked={model.enabled} on:change={onCheckboxChange}/>
    </Loader>
</div>