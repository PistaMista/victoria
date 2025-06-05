<script lang="ts">
    import { BanOutline, CheckCircleOutline, ClockOutline } from "flowbite-svelte-icons";

</script>


<div class="flex justify-center p-2">
    <div class="flex flex-col">
        <div class="flex justify-center text-xl font-bold">
            Monologue Activity
        </div>
        <div class="bg-slate-300 rounded-md flex flex-col p-2 space-y-2">
            <div class="flex bg-slate-400 p-1 rounded-md">
                Check system dashboard
                <div class="grow mx-2"/>
                <ClockOutline/>
            </div>
            <div class="flex bg-slate-400 p-1 rounded-md">
                Answer message
                <div class="grow mx-2"/>
                <CheckCircleOutline/>
            </div>
            <div class="flex bg-slate-400 p-1 rounded-md">
                Generate insight
                <div class="grow mx-2"/>
                <BanOutline/>
            </div>
        </div>
    </div>
</div>