<script lang="ts">
	import { page } from "$app/state";
	import * as Card from "$lib/components/ui/card";
	import { Separator } from "$lib/components/ui/separator";
	import { redirect } from "@sveltejs/kit";
	import type { PageProps } from "./$types";
	import { availableRoles } from "$lib/utils/objects";

    let {data}: PageProps = $props()

    const {employee} = data
</script>

<div class="flex justify-center-safe">
<Card.Root class="basis-1/2">
  <Card.Header>
    <Card.Title class="text-lg">{employee.firstName} {employee.lastName}</Card.Title>
  </Card.Header>
  <Card.Content>
    <Separator class="mb-5" />
    <div class="grid grid-cols-1 gap-3">
      <div class="space-y-2">
        <p class="text-sm font-medium leading-none">Nazwa użytkownika</p>
        <p class="text-muted-foreground text-sm">{employee.username}</p>
      </div>
      <div class="space-y-2">
        <p class="text-sm font-medium leading-none">Email</p>
        <p class="text-muted-foreground text-sm">{employee.email}</p>
      </div>
      <div class="space-y-2">
        <p class="text-sm font-medium leading-none">Rola</p>
        <p class="text-muted-foreground text-sm">{availableRoles.find(ar => ar.id == employee.role)?.label}</p>
      </div>
      {#if employee.employmentDate}
      <div class="space-y-2">
        <p class="text-sm font-medium leading-none">Data zatrudnienia</p>
        <p class="text-muted-foreground text-sm">{Intl.DateTimeFormat("pl-PL", {dateStyle: "long"}).format(Date.parse(employee.employmentDate))}</p>
      </div>
      {/if}
      {#if employee.jobTitle}
      <div class="space-y-2">
        <p class="text-sm font-medium leading-none">Stanowisko</p>
        <p class="text-muted-foreground text-sm">{employee.jobTitle}</p>
      </div>
      {/if}
      {#if employee.department}
      <div class="space-y-2">
        <p class="text-sm font-medium leading-none">Dział</p>
        <p class="text-muted-foreground text-sm">{employee.department}</p>
      </div>
      {/if}
      {#if employee.manager}
      <div class="space-y-2">
        <p class="text-sm font-medium leading-none">Przełożony</p>
        <p class="text-muted-foreground text-sm">{employee.manager.firstName} {employee.manager.lastName}</p>
      </div>
      {/if}
  </div>
  </Card.Content>
  <Card.Footer>
  </Card.Footer>
</Card.Root>
</div>
