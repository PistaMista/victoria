<script lang="ts">
	import { Input } from "flowbite-svelte";
	import LabeledSetting from "../sections/LabeledSetting.svelte";
	import type { PollSettings } from "$lib/types/trigger";
	import ParameterSlider from "../sliders/ParameterSlider.svelte";

	export let settings: PollSettings;
</script>

<div>
	<LabeledSetting label="URL">
		<Input bind:value={settings.url} />
	</LabeledSetting>

	<LabeledSetting label="Interval">
		<ParameterSlider
			label="Interval"
			min={0}
			max={15000}
			fallback={300}
			bind:value={settings.interval}
		/>
	</LabeledSetting>
</div>

