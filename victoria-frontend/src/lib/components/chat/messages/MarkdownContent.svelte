<script lang="ts">
	import type { MarkdownContent } from "$lib/types/message";
	import { parse } from "marked";

	export let content: MarkdownContent;
</script>

<div class="prose">
	{@html parse(content.markdownText)}
</div>

