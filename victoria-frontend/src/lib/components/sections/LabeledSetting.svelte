<script lang="ts">
    import { Label } from "flowbite-svelte";
    export let label: String;
</script>

<div>
    <Label>{label}</Label>                    
    <slot/>
</div>