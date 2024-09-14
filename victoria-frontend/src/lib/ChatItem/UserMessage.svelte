<script lang="ts">
    import { marked } from 'marked';
    export let content = "";
</script>

<div class="p-1 flex flex-row justify-end">
    <div class="p-2 bg-primary-900 text-slate-200 rounded-lg">
        <!-- FIXME: There is totally an XSS attack here -->
        {@html marked(content)}
    </div>
</div>