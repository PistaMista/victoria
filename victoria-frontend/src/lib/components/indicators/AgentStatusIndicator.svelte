<script lang="ts">
    import type { AgentStatus } from "$lib/types/agent";
    export let status: AgentStatus;
    
    let color: string = "";

    $: color = status === 'BUSY' ? "text-orange-500" : "text-lime-500";
</script>

<!-- This is the version shown in AgentCard -->
<div class="font-bold rounded-md bg-black px-2 {color}">
    {status}
</div>