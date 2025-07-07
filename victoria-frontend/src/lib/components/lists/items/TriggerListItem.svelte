<script lang="ts">
    import type { TriggerListItem } from "$lib/types/trigger";
    import { goto } from "$app/navigation";
    
    export let trigger: TriggerListItem;

    function openTriggerDetail() {
        goto(`/admin/triggers/${trigger.id}`);
    }
</script>

<button on:click={openTriggerDetail} class="flex flex-col px-2 my-1 border-t-2 border-black hover:bg-slate-400">
    <div class="flex flex-row">
        <div class="font-bold">
            {trigger.name}
        </div>
        <div class="ml-auto font-bold">
            {trigger.type.toUpperCase()}
        </div>
    </div>
</button>