<script lang="ts">
    import { Popover } from "flowbite-svelte";

    export let justify_end = false;
    export let inner_class = "";
    
    // Hopefully the user does not send multiple messages within a single millisecond
    let msgbox_id = "id" + Date.now().toString();
</script>

<div class="p-1 flex flex-row {justify_end ? "justify-end" : "justify-start"}">
    <div id={msgbox_id} class="p-2 text-slate-200 rounded-lg {inner_class}">
        <slot name="content"/>
    </div>
</div>

<Popover triggeredBy="#{msgbox_id}" trigger="hover" class="p-0">
    <slot name="menu"/>
</Popover>