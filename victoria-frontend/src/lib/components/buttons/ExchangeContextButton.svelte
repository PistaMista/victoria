<script lang="ts">
	export let onclick: () => void;
</script>

<button
	on:click={onclick}
	class="rounded-md hover:bg-slate-500"
	{...$$restProps}
>
	<slot />
</button>

