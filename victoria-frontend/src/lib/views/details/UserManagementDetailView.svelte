<script>
    import UserList from "$lib/components/lists/UserList.svelte";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import DetailView from "$lib/views/DetailView.svelte";
</script>

<DetailView backRoute="/admin">
    <DetailViewSection title="Registered users">
        <UserList/>
    </DetailViewSection>
</DetailView>