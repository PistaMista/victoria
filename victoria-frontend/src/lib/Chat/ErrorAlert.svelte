<script>
    import { Alert } from "flowbite-svelte";
    import { ExclamationCircleOutline } from "flowbite-svelte-icons";
</script>

<Alert>
    <ExclamationCircleOutline class="w-5 h-5"/>
    <span class="font-bold"><slot name="status"/></span>
    <slot name="statusText"/>
</Alert>
