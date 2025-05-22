<script lang="ts" generics="TData, TValue">
	import { Button } from "$lib/components/ui/button";
	import { FlexRender } from "$lib/components/ui/data-table";
	import * as Table from "$lib/components/ui/table";
	import { ChevronLeft, ChevronRight, LoaderCircle } from "@lucide/svelte";
	import { type ColumnDef, type Table as TanStackTable } from "@tanstack/table-core";


    // type DataTableProps<TData, TValue> = {
    //     columns: ColumnDef<TData, TValue>[];
    //     paginatedList: PaginatedList<TData>;
    //     pagination: PaginationStateó
    // }

    // let {paginatedList, columns, pagination = $bindable()}: DataTableProps<TData, TValue> = $props()

  type DataTableProps<TData> = {
    columns: ColumnDef<TData, TValue>[];
    table: TanStackTable<TData>
    isLoading: boolean,
    onRowClick?: (id: number) => void
  }
  let { table, columns, isLoading, onRowClick }: DataTableProps<TData> = $props()
  
  $inspect(isLoading, "isLoading")
</script>


<div class="rounded-md border">
  <Table.Root>
    <Table.Header>
      {#each table.getHeaderGroups() as headerGroup (headerGroup.id)}
        <Table.Row>
          {#each headerGroup.headers as header (header.id)}
            <Table.Head>
              {#if !header.isPlaceholder}
                <FlexRender
                  content={header.column.columnDef.header}
                  context={header.getContext()}
                />
              {/if}
            </Table.Head>
          {/each}
        </Table.Row>
      {/each}
    </Table.Header>
    <Table.Body>
      {#if !isLoading}
        {#each table.getRowModel().rows as row (row.id)}
          <Table.Row 
          data-state={row.getIsSelected() && "selected"}
          class={onRowClick ? "cursor-pointer": ""}
          onclick={() => {
            if(onRowClick) onRowClick(row.getValue("id"))
          }}>
            {#each row.getVisibleCells() as cell (cell.id)}
              <Table.Cell>
                <FlexRender
                  content={cell.column.columnDef.cell}
                  context={cell.getContext()}
                />
              </Table.Cell>
            {/each}
          </Table.Row>
        {:else}
          <Table.Row>
            <Table.Cell colspan={columns.length} class="h-24 text-center">
              Brak wyników
            </Table.Cell>
          </Table.Row>
        {/each}
      {:else}
          <Table.Row>
            <Table.Cell colspan={columns.length} class="h-24 text-center">
               <div class="flex justify-center align-middle mx-0"> <LoaderCircle class="h-10 w-10 animate-spin" /> </div>
            </Table.Cell>
          </Table.Row>
      {/if}
    </Table.Body>
  </Table.Root>
</div>
<div class="flex items-center justify-end space-x-2 py-4">
  <Button
    variant="outline"
    size="sm"
    onclick={() => table.previousPage()}
    disabled={!table.getCanPreviousPage()}
  >
    <ChevronLeft class="h-5 w-5" />
  </Button>
  <div>{table.getState().pagination.pageIndex+1}</div>
  <Button
    variant="outline"
    size="sm"
    onclick={() => table.nextPage()}
    disabled={!table.getCanNextPage()}
  >
    <ChevronRight class="h-5 w-5" />
  </Button>
</div>