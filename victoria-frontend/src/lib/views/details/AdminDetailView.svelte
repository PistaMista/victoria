<script>
    import OptionsRouteButton from "$lib/components/buttons/OptionsRouteButton.svelte";
    import DetailViewSection from "$lib/components/sections/DetailViewSection.svelte";
    import DetailView from "$lib/views/DetailView.svelte";
    import { HammerSolid, CogSolid, RocketSolid, UserSolid } from "flowbite-svelte-icons";
</script>

<DetailView>
    <DetailViewSection title="Administration options">
        <OptionsRouteButton icon={HammerSolid} text="Actions" route="/admin/actions"/>
        <OptionsRouteButton icon={RocketSolid} text="Triggers" route="/admin/triggers"/>
        <OptionsRouteButton icon={UserSolid} text="Users" route="/admin/users"/>
        <OptionsRouteButton icon={CogSolid} text="Settings" route="/admin/settings"/>
    </DetailViewSection>
</DetailView>