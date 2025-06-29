<script lang="ts">
    import { Label } from "flowbite-svelte";
    export let title: String;
</script>
<div>
    <Label class="sticky top-0 bg-white px-2 z-40 font-bold">{title}</Label>
    <div class="bg-slate-400 rounded-md p-2">
        <slot/>
    </div>
</div>