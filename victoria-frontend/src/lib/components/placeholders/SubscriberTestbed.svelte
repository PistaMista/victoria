<script lang="ts">
	import Subscriber from "./Subscriber.svelte";
	import type { TestSubscription } from "$lib/types/websocket";

	let subscription: TestSubscription = {
		type: "test",
		declineRequest: false,
	};

	function handler() {}
</script>

<Subscriber {subscription} {handler}>CHILD</Subscriber>
