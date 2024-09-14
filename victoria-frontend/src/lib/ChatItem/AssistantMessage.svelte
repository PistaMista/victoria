<script lang="ts">
    import { marked } from 'marked';
    export let content = "";
</script>

<div class="p-1 flex flex-row justify-start">
    <div class="p-2 bg-black rounded-lg prose prose-slate-200 text-slate-200">
        <!-- FIXME: There is totally an XSS attack here -->
        {@html marked(content)}
    </div>
</div>