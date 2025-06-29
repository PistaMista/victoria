<script lang="ts">
    export let title: String;
</script>
<div class="flex flex-col m-1">
    <div class="flex justify-center text-xl font-bold">
        {title}
    </div>
    <div class="bg-slate-300 rounded-md flex flex-col p-2 space-y-2">
        <slot/>
    </div>
</div>