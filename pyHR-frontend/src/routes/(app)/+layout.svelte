<script lang="ts">
	import Header from '$lib/components/custom/Header/Header.svelte';
	import NavBar from '$lib/components/custom/NavBar/NavBar.svelte';
	import '../../app.css';
	let { children, data } = $props();
</script>

<div class="bg-muted/40 flex min-h-screen w-full flex-col">
	<aside class="bg-background fixed inset-y-0 left-0 z-10 hidden sm:max-w-xs flex-col border-r rounded-r-2xl sm:flex">
		<NavBar />
	</aside>	
	<div class="flex flex-col sm:gap-4 sm:ml-48">
		<header
		class="bg-background sticky top-0 z-30 flex h-14 items-center gap-4 border-b ml-3 p-3 sm:static sm:h-auto sm:border-0 sm:bg-transparent sm:px-6">
		<Header user={data.user} />
		</header>
		<main
		class="grid flex-1 items-start gap-4 p-4 sm:px-6 sm:py-0 md:gap-8 lg:grid-cols-3 xl:grid-cols-3">
		{@render children()}
		</main>
	</div>
</div>
