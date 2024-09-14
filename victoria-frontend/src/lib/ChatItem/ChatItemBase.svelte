<script lang="ts">
    export let justify_end = false;
    export let inner_class = "";
</script>

<div class="p-1 flex flex-row {justify_end ? "justify-end" : "justify-start"}">
    <div class="p-2 text-slate-200 rounded-lg {inner_class}">
        <slot name="content"/>
    </div>
    <div>
        <slot name="menu"/>
    </div>
</div>