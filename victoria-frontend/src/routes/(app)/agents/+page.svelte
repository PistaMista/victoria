<script>
    import Button from "$lib/components/button/Button.svelte";
    import { Search } from "flowbite-svelte";
    import { DotsVerticalOutline, ClockOutline, CheckCircleOutline, BanOutline, PlusOutline } from "flowbite-svelte-icons";
</script>
<div class="flex flex-col w-full h-full">
    <div class="p-1 bg-slate-400 flex flex-col md:flex-row">
        <Search class="grow max-h-8 md:max-w-72 mb-1 md:mb-0"></Search>
        <div class="mx-2 content-center flex flex-row">
            <div class="hover:bg-slate-300 p-1 rounded-md">
                <Button class="flex flex-row text-nowrap"><PlusOutline class="w-6 h-6"/></Button>
            </div>
        </div>
    </div>

    <div class="flex flex-col md:flex-row md:flex-wrap justify-start p-2">
        <!-- This is an AgentCard -->
        <div class="bg-slate-300 rounded-md p-2 flex flex-col md:w-72 m-1">
            <div class="flex flex-row content-center pl-1 mb-1">
                <div class="font-bold">
                    Researcher
                </div>
                <div class="grow"/>
                <div class="font-bold rounded-md bg-black px-2 text-lime-500">
                    IDLE
                </div>
                <div>
                    <DotsVerticalOutline/>
                </div>
            </div>
            <div class="flex flex-row">
                <div class="bg-orange-200 rounded-md h-14 w-14 p-1"></div>
                <div class="grow h-24 bg-slate-400 rounded-md ml-1 p-1 overflow-y-scroll">
                    <div class="flex flex-col">
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
        </div>

       <div class="bg-slate-300 rounded-md p-2 flex flex-col md:w-72 m-1">
            <div class="flex flex-row content-center pl-1 mb-1">
                <div class="font-bold">
                    Cook
                </div>
                <div class="grow"/>
                <div class="font-bold rounded-md bg-black px-2 text-lime-500">
                    IDLE
                </div>
                <div>
                    <DotsVerticalOutline/>
                </div>
            </div>
            <div class="flex flex-row">
                <div class="bg-orange-200 rounded-md h-14 w-14 p-1"></div>
                <div class="grow h-24 bg-slate-400 rounded-md ml-1 p-1 overflow-y-scroll">
                    <div class="flex flex-col">
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
        </div>
    </div>
</div>