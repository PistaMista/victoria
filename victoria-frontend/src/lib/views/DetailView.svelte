<script lang="ts">
    import BackButton from "$lib/components/buttons/BackButton.svelte";

    export let title: String | null = null;
    export let backRoute: String | null = null;
</script>
<!-- There should be an option to either include or not include a back button -->
<!-- All EditViews should have a creation/editing mode -->

<div class="w-full h-full overflow-y-auto">
    <!-- FIXME: This back button should stay fixed it should not scroll -->
    {#if backRoute}
        <div class="hidden md:inline float-left">
            <BackButton/>
        </div>
    {/if}

    <div class="flex flex-col content-center mx-2 md:m-auto md:max-w-96 space-y-2">
        {#if backRoute}
            <div class="md:hidden">
                <BackButton/>
            </div>            
        {/if}

        {#if title}
            <div class="bg-slate-500 rounded-md w-full text-bold">
                {title}
            </div>
        {/if}
        <slot/>
    </div>
</div>