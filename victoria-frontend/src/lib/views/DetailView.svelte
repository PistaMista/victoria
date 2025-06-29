<script lang="ts">
    export let title: String | null = null;
</script>
<!-- There should be an option to either include or not include a back button -->
<!-- All EditViews should have a creation/editing mode -->

<div class="w-full h-full overflow-y-auto">
    <div class="flex flex-col content-center mx-2 md:m-auto md:max-w-96 space-y-2">
        {#if title}
            <div class="bg-slate-500 rounded-md w-full text-bold">
                {title}
            </div>
        {/if}
        <slot/>
    </div>
</div>