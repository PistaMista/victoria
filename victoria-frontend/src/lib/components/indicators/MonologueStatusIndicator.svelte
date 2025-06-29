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