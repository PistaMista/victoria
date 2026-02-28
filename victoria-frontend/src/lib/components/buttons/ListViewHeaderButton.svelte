<script lang="ts">
	export let onclick: () => void;
</script>

<button
	on:click={onclick}
	class="hover:bg-slate-300 p-1 rounded-md flex flex-row text-nowrap"
	{...$$restProps}><slot /></button
>
