<script lang="ts">
	import * as Breadcrumb  from "$lib/components/ui/breadcrumb";
	import type { UserData } from "$lib/types";
	import { LoaderCircle, User } from "@lucide/svelte";
    import { page } from "$app/state";


    let { user } : { user : Promise<UserData> } = $props();
    console.log(page.url.pathname)
</script>

<Breadcrumb.Root class="hidden md:flex">
    <Breadcrumb.List>
      <Breadcrumb.Item>
        <Breadcrumb.Link href="/">Panel</Breadcrumb.Link>
      </Breadcrumb.Item>
      <Breadcrumb.Separator />
      <Breadcrumb.Item>
        <Breadcrumb.Link href="##">TEST</Breadcrumb.Link>
      </Breadcrumb.Item>
      <Breadcrumb.Separator />
      <Breadcrumb.Item>
        <Breadcrumb.Page>Test</Breadcrumb.Page>
      </Breadcrumb.Item>
    </Breadcrumb.List>
  </Breadcrumb.Root>
<div class="ml-auto md:grow-0 flex items-center gap-1 text-lg">
    {#await user}
        <LoaderCircle class="h-10 w-10 animate-spin" />
    {:then user}
    <User size={28}/> 
    <h4>{user.username}</h4>
    {/await}
</div>
