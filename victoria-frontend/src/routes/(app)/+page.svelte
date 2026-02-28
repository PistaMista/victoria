<script lang="ts">
	import DashboardSection from "$lib/components/sections/DashboardSection.svelte";
</script>

<div class="w-full h-full overflow-y-auto">
	<div class="flex flex-col md:flex-row md:flex-wrap justify-center p-2">
		<DashboardSection title="Activity"></DashboardSection>

		<DashboardSection title="Agents"></DashboardSection>

		<DashboardSection title="Messages"></DashboardSection>
	</div>
</div>

