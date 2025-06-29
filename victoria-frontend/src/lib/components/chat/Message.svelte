<script lang="ts">
    import ActionConfirmationContent from "./messages/ActionConfirmationContent.svelte";
    import MarkdownContent from "./messages/MarkdownContent.svelte";
    import ChoicePromptContent from "./messages/ChoicePromptContent.svelte";
    import ImageContent from "./messages/ImageContent.svelte";
</script>

<div class="flex flex-col">
    <div class="flex flex-row">
        <!-- This is the name of the actor -->
        <div class="font-semibold mr-auto">Researcher</div>
        <!-- This is a DateDisplay -->
        <div class="text-gray-600 text-xs content-center">Today at 10:01 AM</div>                            
    </div>

    <ActionConfirmationContent/>
    <MarkdownContent/>
    <ChoicePromptContent/>
    <ImageContent/>
</div>