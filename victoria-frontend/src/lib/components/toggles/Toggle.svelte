<script lang="ts">
    import { Checkbox } from "flowbite-svelte";
    
    export let label: string;
    export let enabled: boolean = false;
</script>

<div class="flex flex-row m-1 bg-slate-200 rounded-md p-1">
    <div class="font-bold grow">
        {label}
    </div>
    <Checkbox bind:checked={enabled} {...$$restProps}/>
</div>