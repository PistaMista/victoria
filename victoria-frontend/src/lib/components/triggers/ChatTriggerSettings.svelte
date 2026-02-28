<script lang="ts">
	import { Input } from "flowbite-svelte";
	import LabeledSetting from "../sections/LabeledSetting.svelte";
	import type { ChatSettings } from "$lib/types/trigger";

	export let settings: ChatSettings;
</script>

<div>
	<LabeledSetting label="Chat receiver">
		<Input bind:value={settings.receiver} />
	</LabeledSetting>
</div>

