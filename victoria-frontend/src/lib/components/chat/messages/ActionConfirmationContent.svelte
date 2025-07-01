<script lang="ts">
    import { Button, ButtonGroup } from "flowbite-svelte";
    import { ExclamationCircleSolid, CheckOutline, CloseOutline } from "flowbite-svelte-icons";
</script>

<div class="flex flex-col">
    <div class="bg-gradient-to-tr from-red-500 to-orange-500 justify-center flex flex-row font-semibold rounded-md">
        <ExclamationCircleSolid class="mt-0.5 mr-2"/>
        ACTION CONFIRMATION REQUEST
        <ExclamationCircleSolid class="mt-0.5 ml-2"/>
    </div>
    <div class="bg-slate-400 rounded-md my-2 p-2">
        <div class="w-full font-semibold">
            Web search
        </div>
        <ul>
            <li>query: "distance to the moon"</li>
        </ul>
    </div>
    <ButtonGroup class="my-1">
        <Button class="bg-lime-500 grow"><CheckOutline/>EXECUTE</Button>
        <Button class="bg-red-500 grow"><CloseOutline/>ABORT</Button>
    </ButtonGroup>
</div>