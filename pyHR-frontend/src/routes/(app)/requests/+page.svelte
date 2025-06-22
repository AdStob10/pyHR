<script lang="ts">
	import type { SelectOption } from "$lib/components/custom/SelectWrapper/SelectWrapper.svelte";
	import useDataTableStore from "$lib/components/tables/data-table.svelte";
	import DataTable from "$lib/components/tables/DataTable.svelte";
	import FilterDate from "$lib/components/tables/utils/Filters/FilterDate.svelte";
	import FilterSelect from "$lib/components/tables/utils/Filters/FilterSelect.svelte";
	import { type FilterType } from "$lib/components/tables/utils/Filters/filtersUtils";
	import { columns } from "$lib/components/tables/VacationRequestTable/columns.js";
	import { initialFilters } from "$lib/components/tables/VacationRequestTable/filters";
	import { Button, buttonVariants } from "$lib/components/ui/button";
	import * as Collapsible from "$lib/components/ui/collapsible";
	import { createSvelteTable } from "$lib/components/ui/data-table";
	import { statutesAsOptions } from "$lib/utils/objects";
	import { type DateValue } from "@internationalized/date";
	import { getCoreRowModel } from "@tanstack/table-core";
	import type { PageProps } from "../requests/$types";
	import {fly} from "svelte/transition";
	import { ChevronsUpDownIcon } from "@lucide/svelte";
	import AddRequestForm from "$lib/components/custom/Forms/AddRequest/AddRequestForm.svelte";
	import { goto } from "$app/navigation";
	import { Separator } from "$lib/components/ui/separator";



	
    let {data} : PageProps = $props()
	let vacationTypesOptions = $derived(data.vacationTypes.map(t => ({label: t.name, value: t.id} as SelectOption)))
	const hook = useDataTableStore({url: "requests", initialFilters})

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
            return data.vacations.data;
        },
        columns,
        get rowCount() { 
			return data.vacations.rowCount
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


	const onRowClick = (rowid: number) => {
		goto(`/requests/${rowid}`)
	}


	// $inspect(data.vacationTypes, "vacationTypes")

</script>

<h1 class="text-lg">Wnioski urlopowe</h1>
<Separator />


<Collapsible.Root class="w-[180px]">
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
	<div transition:fly={{duration:200}} class="flex justify-items-start gap-2 flex-col">
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
		<div class="flex gap-3">
			<Button variant="outline" class="w-[5rem] border-primary" onclick={async () => await queryData()}>Filtruj</Button>
			<Button variant="secondary" class="w-[5rem] bg-red-800 hover:bg-red-900" onclick={async () => await resetFilters()}>Wyczyść</Button>
		</div>
	</div>
	{/if}
{/snippet}
</Collapsible.Content>
</Collapsible.Root>
<DataTable table={table} columns={columns} isLoading={$isLoading} {onRowClick} />
<div class="flex justify-end">
	<AddRequestForm data={data.form} availableDays={data.availableDays} />
</div>

