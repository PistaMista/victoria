<script lang="ts">
    import { BanOutline, CheckCircleOutline, CheckOutline, ClockOutline, EnvelopeOutline, ExclamationCircleOutline, MailBoxOutline } from "flowbite-svelte-icons";

</script>


<div class="w-full h-full overflow-y-auto">
    <div class="flex flex-col md:flex-row md:flex-wrap justify-center p-2">
        <!-- COMPONENT: DashboardSection -->
        <div class="flex flex-col m-1">
            <div class="flex justify-center text-xl font-bold">
                Monologue Activity
            </div>
            <div class="bg-slate-300 rounded-md flex flex-col p-2 space-y-2">
                <!-- COMPONENT: MonologueMiniCard-->
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

        <!-- COMPONENT: DashboardSection -->
        <div class="flex flex-col m-1">
            <div class="flex justify-center text-xl font-bold">
                Agent Status
            </div>
            <!-- COMPONENT: AgentMiniCard -->
            <div class="bg-slate-300 rounded-md flex flex-col p-2 space-y-2">
                <div class="flex bg-slate-400 p-1 rounded-md">
                    Researcher
                    <div class="grow mx-2"/>
                    <CheckOutline/>
                </div>
                <div class="flex bg-slate-400 p-1 rounded-md">
                    Sysadmin
                    <div class="grow mx-2"/>
                    <ExclamationCircleOutline/>
                </div>
            </div>
        </div>

        <!-- COMPONENT: DashboardSection -->
        <div class="flex flex-col m-1">
            <div class="flex justify-center text-xl font-bold">
                Unread Messages
            </div>
            <div class="bg-slate-300 rounded-md flex flex-col p-2 space-y-2">
                <!-- COMPONENT: UnreadMessageMiniCard -->
                <div class="flex bg-slate-400 p-1 rounded-md">
                    Failed system units
                    <div class="grow mx-2"/>
                    <EnvelopeOutline/>
                </div>
            </div>
        </div>
    </div>
</div>