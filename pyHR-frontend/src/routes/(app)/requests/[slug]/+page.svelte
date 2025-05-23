<script lang="ts">
	import * as Card from "$lib/components/ui/card";
	import { Separator } from "$lib/components/ui/separator";
	import { getVacationDuration, vacationStatuses } from "$lib/utils/objects";
	import { parseDate } from "@internationalized/date";
	import type { PageProps } from "./$types";
	import { LoaderCircle } from "@lucide/svelte";
	import { Button } from "$lib/components/ui/button";
	import { invalidate } from "$app/navigation";


    let { data }: PageProps = $props()
    const {vacation} = data



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
  <Card.Footer>
  </Card.Footer>
</Card.Root>
</div>
{/await}