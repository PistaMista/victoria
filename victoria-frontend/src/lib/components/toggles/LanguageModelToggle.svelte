<script lang="ts">
    import { setModelEnabled } from "$lib/api/models";
    import type { Model } from "$lib/types/model";
    import { Checkbox } from "flowbite-svelte";
    
    export let model: Model;
    
    async function onCheckboxChange() {
        await setModelEnabled(model.id, model.enabled);
    }
</script>

<div class="flex flex-row bg-slate-500 rounded-md p-1">
    <div class="text-white mr-auto">
        {model.name}
    </div>
    <Checkbox bind:checked={model.enabled} on:change={onCheckboxChange}/>
</div>