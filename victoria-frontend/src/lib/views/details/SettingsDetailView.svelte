<script>
	import OptionsRouteButton from "$lib/components/buttons/OptionsRouteButton.svelte";
	import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
	import DetailView from "$lib/views/DetailView.svelte";
	import { LinkOutline, CogSolid, BrainSolid } from "flowbite-svelte-icons";
</script>

<DetailView backRoute="/admin">
	<DetailViewSection title="Settings">
		<OptionsRouteButton
			icon={CogSolid}
			text="General"
			route="/admin/settings/general"
		/>
		<OptionsRouteButton
			icon={LinkOutline}
			text="Connections"
			route="/admin/settings/connections"
		/>
		<OptionsRouteButton
			icon={BrainSolid}
			text="Models"
			route="/admin/settings/models"
		/>
	</DetailViewSection>
</DetailView>

