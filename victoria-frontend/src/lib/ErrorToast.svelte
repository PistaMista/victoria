<script>
    import { Toast } from "flowbite-svelte";
    import { ExclamationCircleOutline } from "flowbite-svelte-icons";
</script>

<Toast color="red">
    <div slot="icon">
        <ExclamationCircleOutline/>
    </div>
    <div class="font-bold">
        <slot name="status"/>
    </div>
    <slot name="statusText"/>
</Toast>