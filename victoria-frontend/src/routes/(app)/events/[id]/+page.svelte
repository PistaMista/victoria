<script>
    import { Label} from "flowbite-svelte";
</script>

<div class="w-full h-full overflow-y-auto">
    <div class="flex flex-col content-center mx-2 md:m-auto md:max-w-96">
        <div class="my-2">
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Trigger</Label>
            <div class="bg-slate-400 rounded-md p-2">
                Receive email
            </div>
        </div>
        <div class="my-2">
            <Label class="sticky top-0 bg-white px-2 z-40 font-bold">Content</Label>
            <div class="bg-slate-400 rounded-md p-2">
                An email was received
            </div>
        </div>
    </div>
</div>
