<script lang="ts">
	import type { SelectOption } from "$lib/components/custom/SelectWrapper/SelectWrapper.svelte";
	import useDataTableStore from "$lib/components/tables/data-table.svelte";
	import DataTable from "$lib/components/tables/DataTable.svelte";
	import { columns } from "$lib/components/tables/SubordinatesVacationRequestTable/columns";
	import { initialFilters } from "$lib/components/tables/SubordinatesVacationRequestTable/filters";
	import FilterDate from "$lib/components/tables/utils/Filters/FilterDate.svelte";
	import FilterSelect from "$lib/components/tables/utils/Filters/FilterSelect.svelte";
	import type { FilterType } from "$lib/components/tables/utils/Filters/filtersUtils";
	import { Button, buttonVariants } from "$lib/components/ui/button";
	import * as Collapsible from "$lib/components/ui/collapsible";
	import { createSvelteTable } from "$lib/components/ui/data-table";
	import { statutesAsOptions } from "$lib/utils/objects";
	import type { DateValue } from "@internationalized/date";
	import { ChevronsUpDownIcon } from "@lucide/svelte";
	import { getCoreRowModel } from "@tanstack/table-core";
	import { fly } from "svelte/transition";
	import type { PageProps } from "./$types";
	import Separator from "$lib/components/ui/separator/separator.svelte";
	import FilterInput from "$lib/components/tables/utils/Filters/FilterInput.svelte";
	import { Toaster } from "$lib/components/ui/sonner";
	import { setContext } from "svelte";



    let { data }: PageProps = $props()
	let subRequests = $derived(data.subRequests?.data)
	setContext("changeSubRequestStatus", (id: number, status: number) => {
		$isLoading = true
		const idx = subRequests.findIndex(s => s.id == id)
		if (subRequests[idx]) {
			const newData = [...subRequests]
			newData[idx].status = status
			subRequests = newData
	
		}
		$isLoading = false
	})
    const hook = useDataTableStore({url: "subordinates/requests", initialFilters})
    let vacationTypesOptions = $derived(data.vacationTypes.map(t => ({label: t.name, value: t.id} as SelectOption)))
    
    const {
		pagination,
		sorting,
		filters,
		isLoading,
		queryData,
		queryDataAfterPageChange,
		resetFilters,
		updateFilterByName,
		updateFilterTypeByName,
	} = hook


    const table = createSvelteTable({
        get data() {
            return subRequests;
        },
        columns,
        get rowCount() { 
			return data.subRequests.rowCount
		},
        state: {
          get pagination() {
            return $pagination
          },
		  get sorting() {
			return $sorting
		  }
        },
        manualPagination: true,
		manualFiltering: true,
        onPaginationChange: async (updater) => {
          if (typeof updater === "function") {
            pagination.set(updater($pagination))
          } else {
            pagination.set(updater);
          }

          await queryDataAfterPageChange()
        },
		onSortingChange: async (updater) => {
          if (typeof updater === "function") {
            sorting.set(updater($sorting))
          } else {
            sorting.set(updater);
          }
		//   console.log($sorting)
		  await queryDataAfterPageChange()
        },
        getCoreRowModel: getCoreRowModel(),
    });


    // $inspect("data", subRequests)

</script>


<h1 class="text-lg">Wnioski pracowników</h1>
<Separator />
<!-- {#await data.vacations} 
   <div class="flex justify-center align-middle mx-0"> <LoaderCircle class="h-10 w-10 animate-spin" /> </div>
{:then resolved} -->
<Collapsible.Root>
	<div class="flex items-center space-x-4">
		<h3 class="text-sm font-semibold">Filtry</h3>
		<Collapsible.Trigger
		class={buttonVariants({ variant: "ghost", size: "sm", class: "w-9 p-0" })}
		>
		<ChevronsUpDownIcon />
		<span class="sr-only">Otwórz</span>
		</Collapsible.Trigger>
  	</div>
<Collapsible.Content forceMount>
{#snippet child({ props, open })}
	{#if open}
	<div transition:fly={{duration:200}} class="flex justify-items-start gap-2 flex-col mt-2">
		<FilterSelect 
			options={statutesAsOptions()} 
			selected={$filters["status"]} 
			onValueChangeFn={(val: string) => updateFilterByName("status", val)} 
			placeholder="Wybierz status..."
			classValues={["w-[180px]"]}
		/>
		<div class="flex gap-3">
			<FilterDate 
				filter={$filters["startDate"]}
				onTypeChangeFn={(val: FilterType) => updateFilterTypeByName("startDate", val)}
				onValueChangeFn={(val: DateValue | undefined) => updateFilterByName("startDate", val)} 
			/>
			<FilterDate 
				filter={$filters["endDate"]}
				onTypeChangeFn={(val: FilterType) => updateFilterTypeByName("endDate", val)}
				onValueChangeFn={(val: DateValue | undefined) => updateFilterByName("endDate", val)} 
			/>
		</div>
		<FilterSelect
			options={vacationTypesOptions}
			selected={$filters["vacationType"]}
			onValueChangeFn={(val: string) => updateFilterByName("vacationType", val)} 
			placeholder="Wybierz rodzaj urlopu..."
			classValues={["w-[200px]"]}
		/>
        <div>
            <p class="my-3 text-muted-foreground">Pracownik</p>
            <div class="flex gap-3 grow">
                <FilterInput bind:value={$filters.firstName.value} label="Imię" />
                <FilterInput bind:value={$filters.lastName.value} label="Nazwisko" />
            </div>
        </div>
		<div class="flex gap-3">
			<Button variant="secondary" class="w-[5rem] border-primary" onclick={async () => await queryData()}>Filtruj</Button>
			<Button variant="secondary" class="w-[5rem] bg-red-800 hover:bg-red-900" onclick={async () => await resetFilters()}>Wyczyść</Button>
		</div>
	</div>
	{/if}
{/snippet}
</Collapsible.Content>
</Collapsible.Root>
<DataTable table={table} columns={columns} isLoading={$isLoading} />
<Toaster />

