<script lang='ts'>
	import useDataTableStore from "$lib/components/tables/data-table.svelte";
	import { columns } from "$lib/components/tables/SubordinatesTable/columns";
	import { initialFilters } from "$lib/components/tables/SubordinatesTable/filters";
	import { createSvelteTable } from "$lib/components/ui/data-table";
	import { getCoreRowModel } from "@tanstack/table-core";
	import type { PageProps } from "./$types";
	import { Separator } from "$lib/components/ui/separator";
	import * as Collapsible from "$lib/components/ui/collapsible";
	import FilterInput from "$lib/components/tables/utils/Filters/FilterInput.svelte";
	import { Button, buttonVariants } from "$lib/components/ui/button";
	import { fly } from "svelte/transition";
	import { ChevronsUpDownIcon } from "@lucide/svelte";
	import DataTable from "$lib/components/tables/DataTable.svelte";
	import { Toaster } from "$lib/components/ui/sonner";
	import FilterDate from "$lib/components/tables/utils/Filters/FilterDate.svelte";
	import type { FilterType } from "$lib/components/tables/utils/Filters/filtersUtils";
	import type { DateValue } from "@internationalized/date";
	import { goto } from "$app/navigation";
	import AddEmployeeForm from "$lib/components/custom/Forms/AddEmployee/AddEmployeeForm.svelte";



    let { data }: PageProps = $props()
    const hook = useDataTableStore({url: "subordinates", initialFilters})

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
            return data.employees.data;
        },
        columns,
        get rowCount() { 
			return data.employees.rowCount
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
		goto(`/users/${rowid}`)
	}


</script>



<h1 class="text-lg">Pracownicy</h1>
<Separator />
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
        <div class="flex gap-3 grow">
            <FilterInput bind:value={$filters.firstName.value} label="Imię" />
            <FilterInput bind:value={$filters.lastName.value} label="Nazwisko" />
        </div>
        <FilterInput className="max-w-md" bind:value={$filters.jobTitle.value} label="Stanowisko" />
        <FilterInput className="max-w-md" bind:value={$filters.department.value} label="Dział" />
        <FilterDate 
				filter={$filters["employmentDate"]}
				onTypeChangeFn={(val: FilterType) => updateFilterTypeByName("employmentDate", val)}
				onValueChangeFn={(val: DateValue | undefined) => updateFilterByName("employmentDate", val)} 
        />
		<div class="flex gap-3 mt-2">
			<Button variant="secondary" class="w-[5rem] border-primary" onclick={async () => await queryData()}>Filtruj</Button>
			<Button variant="secondary" class="w-[5rem] bg-red-800 hover:bg-red-900" onclick={async () => await resetFilters()}>Wyczyść</Button>
		</div>
	</div>
	{/if}
{/snippet}
</Collapsible.Content>
</Collapsible.Root>
<DataTable table={table} columns={columns} isLoading={$isLoading} {onRowClick} />
<Toaster />
<div class="flex justify-end">
	<Button href="/subordinates/add" class="w-[10rem] mb-5">Nowy pracownik</Button>
</div>


