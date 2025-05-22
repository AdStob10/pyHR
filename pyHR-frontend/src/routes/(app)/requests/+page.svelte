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
	import AddRequestForm from "$lib/components/custom/Forms/AddRequestForm.svelte";
	import { goto } from "$app/navigation";



	/*

	 url: string,
    columns: ColumnDef<T>[],   
    pageData: PaginatedList<T>,
    initialFilters: Record<string, FilterItem>

	*/

	
    let {data} : PageProps = $props()
	// let pagination = $state<PaginationState>({pageIndex: 0, pageSize: 2})
	// let filters = $state<Record<string, FilterItem>>(initialFilters)
	// let isLoading = $state(false)
	let vacationTypesOptions = $derived(data.vacationTypes.map(t => ({label: t.name, value: t.id} as SelectOption)))
	//const hook = useDataTable("requests", initialFilters)
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

	// const {
	// 	getPagination,
	// 	filters,
	// 	isLoading,
	// 	queryData,
	// 	queryDataAfterPageChange,
	// 	resetFilters,
	// 	filterByName,
	// 	updateFilterByName,
	// 	updateFilterTypeByName,
	// 	setPagination
	// } = hook

	// const queryData = async () => {
	// 		let params = new URLSearchParams()
	// 		params = setFiltersOnParams(filters, params)
	// 		params.set("offset", "0")
	// 		params.set("limit", pagination.pageSize.toString())
	// 		pagination.pageIndex = 0
	// 		pagination.pageSize = 2

	// 		isLoading = true
	// 		await goto("/requests?"+params, {replaceState: false, keepFocus: true, noScroll: true})
	// 		isLoading = false
	// 	}


	// const queryDataAfterPageChange =  async () => {
	// 		let params = new URLSearchParams()
	// 		const offset = pagination.pageIndex * pagination.pageSize
	// 		params.set("offset", offset.toString())
	// 		params.set("limit", pagination.pageSize.toString())
	// 		params = setFiltersOnParams(filters, params)
			
	// 		isLoading = true
	// 		await goto("/requests?"+params, {replaceState: false, keepFocus: true, noScroll: true})
	// 		isLoading = false
	// 	}
	

	// const resetFilters = async () => {
	// 		let params = new URLSearchParams()
	// 		params.set("offset", "0")
	// 		params.set("limit", pagination.pageSize.toString())
	// 		pagination.pageIndex = 0
	// 		pagination.pageSize = 2
	// 		filters = initialFilters
			
	// 		isLoading = true
	// 		await goto("/requests?"+params, {replaceState: false, keepFocus: true, noScroll: true})
	// 		isLoading = false
	// 	}



	// const filterByName = (name: string) => {
	// 	return filters[name]
	// }

	// const updateFilterByName = (name: string, value: any) => {
	// 	const filter = filterByName(name)
	// 	filter.value = value
	// }

	// const updateFilterTypeByName = (name: string, value: FilterType) => {
	// 	const filter = filterByName(name)
	// 	filter.type = value
	// }


	// const table = createSvelteTable({
    //     get data() {
    //         return data.vacations.data;
    //     },
    //     columns,
    //     get rowCount() { 
	// 		return data.vacations.rowCount
	// 	},
    //     state: {
    //       get pagination() {
    //         return pagination
    //       }
    //     },
    //     manualPagination: true,
	// 	manualFiltering: true,
    //     onPaginationChange: async (updater) => {
    //       if (typeof updater === "function") {
    //         pagination = updater(pagination)
    //       } else {
    //         pagination = updater;
    //       }

    //       await queryDataAfterPageChange()
    //     },
    //     getCoreRowModel: getCoreRowModel(),
    // });

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
		  console.log($sorting)
		  await queryDataAfterPageChange()
        },
        getCoreRowModel: getCoreRowModel(),
    });


	const onRowClick = (rowid: number) => {
		goto(`/requests/${rowid}`)
	}


	// const table = createSvelteTable({
    //     get data() {
    //         return data.vacations.data;
    //     },
    //     columns,
    //     get rowCount() { 
	// 		return data.vacations.rowCount
	// 	},
    //     state: {
    //       get pagination() {
    //         return getPagination()
    //       }
    //     },
    //     manualPagination: true,
	// 	manualFiltering: true,
    //     onPaginationChange: async (updater) => {
    //       if (typeof updater === "function") {
    //         setPagination(updater(getPagination()))
    //       } else {
    //         setPagination(updater);
    //       }

    //       await queryDataAfterPageChange()
    //     },
    //     getCoreRowModel: getCoreRowModel(),
    // });


	//$inspect(pagination, "paginationState")
	//$inspect($filters, "filters")	
	//$inspect(data, "data")
	$inspect(data.vacationTypes, "vacationTypes")
	// $inspect(table.options.rowCount, "rowCount")	

</script>

<h4>Wnioski urlopowe</h4>

<!-- {#await data.vacations} 
   <div class="flex justify-center align-middle mx-0"> <LoaderCircle class="h-10 w-10 animate-spin" /> </div>
{:then resolved} -->
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
			<Button variant="outline" class="w-[5rem] hover:bg-red-500 border-red-500" onclick={async () => await resetFilters()}>Wyczyść</Button>
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
<!-- {/await} -->

