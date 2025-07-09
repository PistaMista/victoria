<script lang="ts">
    import LabeledSetting from "../sections/LabeledSetting.svelte";
    import type { TimerSettings } from "$lib/types/trigger";
    import ParameterSlider from "../sliders/ParameterSlider.svelte";
    
    export let settings: TimerSettings;
</script>

<div>
    <LabeledSetting label="Interval">
        <ParameterSlider
            aria-label="Interval"
            label="Interval"
            min={0}
            max={15000}
            fallback={300}
            bind:value={settings.interval}
        />
    </LabeledSetting>
</div>