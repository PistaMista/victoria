<script lang="ts">
    import { parse } from 'marked';
    export let content = "";
    let parsed = "";

    $: {
        let res = parse(content);
        if (res instanceof Promise) {
            res.then((t) => parsed = t);
        } else {
            parsed = res;
        }
    }
</script>

<div class="p-1 flex flex-row justify-start">
    <div class="p-2 bg-black rounded-lg prose prose-slate">
        {@html parsed}
    </div>
</div>