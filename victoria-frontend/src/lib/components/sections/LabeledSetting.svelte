<script lang="ts">
	import { Label } from "flowbite-svelte";
	export let label: string;
</script>

<div>
	<Label>{label}</Label>
	<div aria-label={label}>
		<slot />
	</div>
</div>

