<script lang="ts">
    import AgentMiniCard from "$lib/components/cards/AgentMiniCard.svelte";
    import MonologueMiniCard from "$lib/components/cards/MonologueMiniCard.svelte";
    import UnreadMessageMiniCard from "$lib/components/cards/UnreadMessageMiniCard.svelte";
    import DashboardSection from "$lib/components/sections/DashboardSection.svelte";
</script>

<div class="w-full h-full overflow-y-auto">
    <div class="flex flex-col md:flex-row md:flex-wrap justify-center p-2">
        <DashboardSection title="Activity">
            <MonologueMiniCard/>
            <MonologueMiniCard/>
            <MonologueMiniCard/>
        </DashboardSection>
        
        <DashboardSection title="Agents">
            <AgentMiniCard/>
            <AgentMiniCard/>
            <AgentMiniCard/>
        </DashboardSection>
        
        <DashboardSection title="Messages">
            <UnreadMessageMiniCard/>
            <UnreadMessageMiniCard/>
            <UnreadMessageMiniCard/>
        </DashboardSection>
    </div>
</div>