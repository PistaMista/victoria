<script>
    import { ClockOutline, RocketOutline, CheckOutline } from "flowbite-svelte-icons";
</script>

<!-- COMPONENT: MonologueStatusIndicator -->
<!-- This is the long horizontal version shown in MonologueDetailView -->
<div class="flex flex-row">
    <div class="bg-black rounded-md px-1 font-bold text-lime-500">RUNNING</div>
    <div class="grow"/>
    <div class="mx-1 flex flex-row">
        <ClockOutline/>
        20m39s
    </div>
    <div class="px-1 border-l-2 flex flex-row">
        <RocketOutline/>
        20m
    </div>
    <div class="px-1 border-l-2 flex flex-row">
        <CheckOutline/>
        20m
    </div>
</div>

<!-- This is the short vertical version shown in MonologueListItem -->
<div class="flex flex-col">
    <div class="font-bold text-lime-600 rounded-md bg-slate-600 p-1">
        RUNNING
    </div>
    <div class="text-center">
        20m39s
    </div>
</div>