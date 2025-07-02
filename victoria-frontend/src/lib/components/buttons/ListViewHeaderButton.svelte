<script lang="ts">
    import { Button } from "flowbite-svelte";
</script>

<div class="hover:bg-slate-300 p-1 rounded-md" {...$$restProps}>
    <Button class="flex flex-row text-nowrap"><slot/></Button>
</div>