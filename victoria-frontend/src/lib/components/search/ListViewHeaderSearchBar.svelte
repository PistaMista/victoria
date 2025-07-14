<script lang="ts">
    import { Search } from "flowbite-svelte";
    
    export let onsubmit: (val: string) => void = () => {};
    export let ontype: (val: string) => void = () => {};
    export let debounce: number = 300;
    
    let value = "";
    let timeout: number;
    
    function submit() {
        onsubmit(value);
    }
    
    function oninput() {
        clearTimeout(timeout);
        timeout = setTimeout(() => {ontype(value)}, debounce);
    }
</script>

<form on:submit={submit}>
    <Search 
        role="search" 
        class="grow max-h-8 md:max-w-72 mb-1 md:mb-0" 
        bind:value 
        on:input={oninput}
    />
</form>