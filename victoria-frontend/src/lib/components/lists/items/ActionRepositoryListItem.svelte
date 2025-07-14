<script lang="ts">
    import type { ActionRepository } from "$lib/types/action_repo";
    import { goto } from "$app/navigation";
    
    export let repository: ActionRepository;
    
    function openRepositoryDetail() {
        goto(`/admin/actions/${repository.id}/edit`);
    }
</script>

<button on:click={openRepositoryDetail} class="flex flex-col px-2 my-1 border-t-2 border-black hover:bg-slate-400">
    <div class="font-bold">
        {repository.name}
    </div>
    <div>
        URL: {repository.url}
    </div>
</button>