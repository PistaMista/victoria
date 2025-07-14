<script lang="ts">
    import LabeledSetting from "../sections/LabeledSetting.svelte";
    import { Textarea } from "flowbite-svelte";
    
    
    export let variables: string[];
    export let template: string;
    
    const varRegex = /\$\((\w+)\)/g;
    
    function getUndefinedVars(text: string) {
        const res: string[] = [];
        const matches = [...text.matchAll(varRegex)];

        for (const match of matches) {
            if (!variables.includes(match[1])) {
                res.push(match[1]);
            }
        }
        
        return res;
    }
    $: undefinedVariables = getUndefinedVars(template);

</script>

<div>
    <LabeledSetting label="Parser variables">
        {#each variables as variable}
            <div class="m-0.5 font-bold text-orange-500">
                $({variable})
            </div>
        {/each}
    </LabeledSetting>
    
    <LabeledSetting label="Event template">
        <Textarea aria-label="Template" bind:value={template}/>
    </LabeledSetting>
    
    {#if undefinedVariables.length > 0}
        <LabeledSetting label="Errors">
            <div class="flex flex-col">
                {#each undefinedVariables as variable}
                    <div class="font-bold text-red-500">
                        Error: undefined variable '{variable}'
                    </div>
                {/each}
            </div>
        </LabeledSetting>
    {/if}
</div>
