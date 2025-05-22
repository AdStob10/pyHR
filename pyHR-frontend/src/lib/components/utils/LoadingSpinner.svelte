<script lang="ts">
	import { LoaderCircle } from "@lucide/svelte";


let {children, promise} = $props()
</script>



{#await promise}
    <LoaderCircle class="h-10 w-10 animate-spin" />
{:then data}
{@render children(data)}
{/await}