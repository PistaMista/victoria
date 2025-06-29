<!-- These "thought cards" should be collapsible - the thoughts can be quite long -->
<script lang="ts">
    import ActionContent from "./thoughts/ActionContent.svelte";
    import FailureContent from "./thoughts/FailureContent.svelte";
    import SuccessContent from "./thoughts/SuccessContent.svelte";
    import TriggerContent from "./thoughts/TriggerContent.svelte";
    import VerbatimContent from "./thoughts/VerbatimContent.svelte";
</script>

<div class="rounded-md z-20 bg-slate-200 p-2">
    <ActionContent/>
    <FailureContent/>
    <SuccessContent/>
    <TriggerContent/>
    <VerbatimContent/>
</div>