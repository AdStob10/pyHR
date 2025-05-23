<script lang="ts">
 import { invalidate } from "$app/navigation";
 import { Button } from "$lib/components/ui/button/index.js";
 import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
 import EllipsisIcon from "@lucide/svelte/icons/ellipsis";
	import { getContext } from "svelte";
 import { toast } from "svelte-sonner";

 let { id, statusId }: { id: number, statusId: number } = $props();
 const changeFn: (id: number, statusId: number) => void = getContext("changeSubRequestStatus")

 export const acceptRequest = async (id: number) => {
   const request = fetch(`/api/vacation/requests/${id}/status?status=1`, {
      method: "POST"
   })
   toast.promise(request, {
      loading: 'Czekaj...',
      success: () => {
         changeFn(id, 1)
         return `Wniosek nr ${id} zaakceptowany`;
      },
      error: 'Wystąpił błąd przy akcpetacji wniosku',
   });
 }

  export const rejectRequest = async (id: number) => {
   const request = fetch(`/api/vacation/requests/${id}/status?status=2`, {
      method: "POST"
   })
   toast.promise(request, {
      loading: 'Czekaj...',
      success: () => {
         changeFn(id, 2)
         return `Wniosek nr ${id} odrzucony`;
      },
      error: 'Wystąpił błąd przy odrzucaniu wniosku',
   });
 }

</script>
 
<DropdownMenu.Root>
 <DropdownMenu.Trigger>
  {#snippet child({ props })}
   <Button
    {...props}
    variant="ghost"
    size="icon"
    class="relative size-8 p-0"
   >
    <span class="sr-only">Otwórz menu</span>
    <EllipsisIcon />
   </Button>
  {/snippet}
 </DropdownMenu.Trigger>
 <DropdownMenu.Content>
  <DropdownMenu.Group>
   <DropdownMenu.Label>Akcje</DropdownMenu.Label>
   <DropdownMenu.Item onclick={() => navigator.clipboard.writeText(id.toString())}>
    Skopiuj id
   </DropdownMenu.Item>
  </DropdownMenu.Group>
  <DropdownMenu.Separator />
  <DropdownMenu.Item><a href={`/subordinates/requests/${id}`}>Przejdź do wniosku</a></DropdownMenu.Item>
  {#if statusId == 0}
   <DropdownMenu.Item  onclick={() => acceptRequest(id)}>Zaakceptuj wniosek</DropdownMenu.Item>
  {/if}
  {#if statusId !== 2}
   <DropdownMenu.Item onclick={() => rejectRequest(id)}>Odrzuć wniosek</DropdownMenu.Item>
  {/if}
 </DropdownMenu.Content>
</DropdownMenu.Root>