<script lang="ts">
	import * as Breadcrumb  from "$lib/components/ui/breadcrumb";
	import type { UserData, UserWithRole } from "$lib/types";
	import { LoaderCircle, User } from "@lucide/svelte";
  import { page } from "$app/state";


  let { user } : { user : UserWithRole } = $props();
  const urls = $derived.by(() => {
    let url = page.url.protocol
    const splitted = page.url.pathname.split("/").map((val) => {
      url += val + "/"
      val = val.charAt(0).toUpperCase() + val.slice(1)
      return {label: val, href: url}
    }).filter(val => val.label != "")
    return splitted
  })


</script>

<Breadcrumb.Root class="hidden md:flex">
    <Breadcrumb.List>
      <Breadcrumb.Item>
        <Breadcrumb.Link href="/">Panel</Breadcrumb.Link>
      </Breadcrumb.Item>
      {#each urls as u}
      <Breadcrumb.Separator />
      <Breadcrumb.Item>
        <Breadcrumb.Link href={u.href}>{u.label}</Breadcrumb.Link>
      </Breadcrumb.Item>  
      {/each}
    </Breadcrumb.List>
  </Breadcrumb.Root>
<div class="ml-auto md:grow-0 flex items-center gap-1 text-lg">
    <!-- {#await user}
        <LoaderCircle class="h-10 w-10 animate-spin" />
    {:then user} -->
    <User size={28}/> 
    <h4>{`${user.firstName} ${user.lastName}`}</h4>
    <!-- {/await} -->
</div>
