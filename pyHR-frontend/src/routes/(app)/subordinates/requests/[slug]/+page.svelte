<script lang="ts">

	import * as Card from "$lib/components/ui/card";
	import { Separator } from "$lib/components/ui/separator";
	import { getVacationDuration, vacationStatuses } from "$lib/utils/objects";
	import { LoaderCircle } from "@lucide/svelte";
	import type { PageProps } from "./$types";
	import { Button } from "$lib/components/ui/button";
	import { toast } from "svelte-sonner";
	import { invalidate } from "$app/navigation";
	import { Toaster } from "$lib/components/ui/sonner";


  let { data }: PageProps = $props()
  let vacation = $derived(data.vacation)


  export const acceptRequest = async (id: number) => {
    const request = fetch(`/api/vacation/requests/${id}/status?status=1`, {
        method: "POST"
    })
    toast.promise(request, {
        loading: 'Czekaj...',
        success: () => {
          vacation = {...vacation, status: 1}
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
        vacation = {...vacation, status: 2}
        return `Wniosek nr ${id} odrzucony`;
      },
      error: 'Wystąpił błąd przy odrzucaniu wniosku',
    });
  }

  $inspect("vacation", vacation)
</script>

{#await vacation} 
   <div class="flex justify-center align-middle mx-0"> <LoaderCircle class="h-10 w-10 animate-spin" /> </div>
{:then data}
{@const Icon = vacationStatuses.find(vs => vs.id == data.status)?.icon}
<div class="flex justify-center-safe">
<Card.Root class="basis-1/2">
  <Card.Header>
    <Card.Title class="text-lg">Wniosek Urlopowy {data.id}</Card.Title>
  </Card.Header>
  <Card.Content>
    <Separator class="mb-5" />
      <div class="grid grid-cols-1 gap-3">
        <div class="space-y-2">
          <p class="text-sm font-medium leading-none">Pracownik</p>
          <p class="text-muted-foreground text-sm">{data.employee.firstName + " " + data.employee.lastName}</p>
        </div>
        <div class="space-y-2">
          <p class="text-sm font-medium leading-none">Początek</p>
          <p class="text-muted-foreground text-sm">{data.startDate}</p>
        </div>
        <div class="space-y-2">
          <p class="text-sm font-medium leading-none">Koniec</p>
          <p class="text-muted-foreground text-sm">{data.endDate}</p>
        </div>
        <div class="space-y-2">
          <p class="text-sm font-medium leading-none">Ilość dni</p>
          <p class="text-muted-foreground text-sm">{getVacationDuration(data.startDate, data.endDate)}</p>
        </div>
        <div class="space-y-2">
          <p class="text-sm font-medium leading-none">Rodzaj urlopu</p>
          <p class="text-muted-foreground text-sm">{data.vacationType.name}</p>
        </div>
        <div class="space-y-2">
          <p class="text-sm font-medium leading-none">Status</p>
          <div class="flex items-center">
            <Icon class="mr-2 h-2 w-2" />
            <span class="text-muted-foreground text-sm">{vacationStatuses.find(vs => vs.id == data.status)?.name}</span>
          </div>
        </div>
        {#if data.reason}
        <div class="space-y-2">
          <p class="text-sm font-medium leading-none">Powód</p>
          <p class="text-muted-foreground text-sm">{data.reason}</p>
        </div>
        {/if}
      </div>
  </Card.Content>
  <Card.Footer class="flex gap-3 justify-end">
    {#if data.status == 0}
      <Button variant="secondary" class="w-[5rem]" onclick={() => acceptRequest(data.id)}>Zatwierdź</Button>
    {/if}
    {#if data.status != 2}
      <Button variant="secondary" class="w-[5rem] bg-red-800 hover:bg-red-900" onclick={() => rejectRequest(data.id)}>Odrzuć</Button>
    {/if}
  </Card.Footer>
</Card.Root>
<Toaster />
</div>
{/await}