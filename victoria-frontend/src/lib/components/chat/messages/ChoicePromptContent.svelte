<script lang="ts">
    import { ExclamationCircleSolid } from "flowbite-svelte-icons";
    import { Button } from "flowbite-svelte";
</script>

<div class="flex flex-col">
    <div class="bg-gradient-to-tr from-red-500 to-orange-500 justify-center flex flex-row font-semibold rounded-md">
        <ExclamationCircleSolid class="mt-0.5 mr-2"/>
        CHOICE REQUIRED
        <ExclamationCircleSolid class="mt-0.5 ml-2"/>
    </div>
    <div class="text-center">
        Please choose an account to sign into
    </div>

    <div class="flex flex-col space-y-2 rounded-md p-2 m-1 bg-slate-500">
        <Button class="w-full">This one</Button>
        <Button class="w-full">That one</Button>
    </div>
</div>