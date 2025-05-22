// src/lib/hooks/useDataTable.svelte.ts

import { goto } from '$app/navigation'
import { getCoreRowModel, type ColumnDef, type PaginationState } from '@tanstack/table-core'
import { setFiltersOnParams, type FilterItem, type FilterType } from './utils/Filters/filtersUtils'
import { createSvelteTable } from '../ui/data-table'
import type { PaginatedList } from '$lib/types'

export default function useDataTable<T>(
  url: string,
  getTableData: () => PaginatedList<T>,
  columns: ColumnDef<T>[],
  initialFilters: Record<string, FilterItem>,
  pageSize = 2
) {
  // Reactive states
  let pagination  = $state<PaginationState>({ pageIndex: 0, pageSize })
  let filters = $state<Record<string, FilterItem>>({ ...initialFilters })
  let isLoading = $state(false)

  	const queryData = async () => {
			let params = new URLSearchParams()
			params = setFiltersOnParams(filters, params)
			params.set("offset", "0")
			params.set("limit", pagination.pageSize.toString())

			isLoading = true
			await goto("/requests?"+params, {replaceState: false, keepFocus: true, noScroll: true})
			isLoading = false
		}


	const queryDataAfterPageChange =  async () => {
			let params = new URLSearchParams()
			const offset = pagination.pageIndex * pagination.pageSize
			params.set("offset", offset.toString())
			params.set("limit", pagination.pageSize.toString())
			params = setFiltersOnParams(filters, params)
			
			isLoading = true
			await goto("/requests?"+params, {replaceState: false, keepFocus: true, noScroll: true})
			isLoading = false
		}
	

	const resetFilters = async () => {
			const params = new URLSearchParams()
			params.set("offset", "0")
			params.set("limit", pagination.pageSize.toString())
			filters = initialFilters
			
			isLoading = true
			await goto("/requests?"+params, {replaceState: false, keepFocus: true, noScroll: true})
			isLoading = false
		}

  const getPagination = () => pagination
  const setPagination = (pag: PaginationState) => pagination = pag

	
  // Helpers to manipulate filters
  const filterByName = (name: string) => filters[name]

  const updateFilterByName = (name: string, value: unknown) => {
    filters[name].value = value
  }

  const updateFilterTypeByName = (name: string, value: FilterType) => {
    filters[name].type = value
  }

  const table = createSvelteTable({
      get data() {
        return getTableData().data
      },
        columns,
      get rowCount() { 
			  return getTableData().rowCount
		  },
        state: {
          get pagination() {
            return pagination
          }
        },
        manualPagination: true,
		manualFiltering: true,
        onPaginationChange: async (updater) => {
          if (typeof updater === "function") {
            pagination = updater(pagination)
          } else {
            pagination = updater
          }

          await queryDataAfterPageChange()
        },
        getCoreRowModel: getCoreRowModel(),
    });


  return {
	table,
    getPagination,
    filters,
    isLoading,
    queryData,
    queryDataAfterPageChange,
    resetFilters,
    filterByName,
    updateFilterByName,
    updateFilterTypeByName,
	setPagination
  }
}
