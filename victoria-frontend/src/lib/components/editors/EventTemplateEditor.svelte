<script>
    import LabeledSetting from "../sections/LabeledSetting.svelte";
    import { Textarea } from "flowbite-svelte";
</script>
<div>
    <LabeledSetting label="Parser variables">
        <div class="m-0.5 font-bold text-orange-500">
            $content
        </div>

        <div class="m-0.5 font-bold text-orange-500">
            $key
        </div>
    </LabeledSetting>
    
    <LabeledSetting label="Event template">
        <Textarea/>
    </LabeledSetting>
</div>
