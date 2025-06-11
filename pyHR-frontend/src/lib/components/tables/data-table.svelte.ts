// lib/hooks/useDataTable.ts
import { writable, get } from 'svelte/store';
import { goto } from '$app/navigation';
import { type PaginationState, type SortingState } from '@tanstack/table-core';

import { setFiltersOnParams, type FilterItem, type FilterType } from './utils/Filters/filtersUtils';
import { setSortingOnParams } from './utils/Sort/sortUtils';


export type CreateDataTableParams = {
  url: string;
  initialFilters: Record<string, FilterItem>;
};

export default function useDataTableStore({ url,  initialFilters }: CreateDataTableParams) {
  const pagination = writable<PaginationState>({ pageIndex: 0, pageSize: 5 });
  const sorting = writable<SortingState>([])
  const filters = writable<Record<string, FilterItem>>({ ...initialFilters });
  const isLoading = writable(false);

  async function queryData() {
    const paginationVal = get(pagination);
    const filtersVal = get(filters);

    const params = setFiltersOnParams(filtersVal, new URLSearchParams());
    params.set('offset', '0');
    params.set('limit', paginationVal.pageSize.toString());

    pagination.set({ ...paginationVal, pageIndex: 0 });
    isLoading.set(true);
    await goto(`/${url}?` + params, { replaceState: false, keepFocus: true, noScroll: true });
    isLoading.set(false);
  }

  async function queryDataAfterPageChange() {
    const paginationVal = get(pagination);
    const filtersVal = get(filters);
    const sortingVal = get(sorting);

    const offset = paginationVal.pageIndex * paginationVal.pageSize;
    let params = setFiltersOnParams(filtersVal, new URLSearchParams());
    params = setSortingOnParams(sortingVal, params)
    params.set('offset', offset.toString());
    params.set('limit', paginationVal.pageSize.toString());

    isLoading.set(true);
    await goto(`/${url}?` + params, { replaceState: false, keepFocus: true, noScroll: true });
    isLoading.set(false);
  }

  async function resetFilters() {
    const paginationVal = get(pagination);

    const params = new URLSearchParams();
    params.set('offset', '0');
    params.set('limit', paginationVal.pageSize.toString());

    pagination.set({ ...paginationVal, pageIndex: 0 });
    filters.update((f) => {
      Object.keys(f).forEach(k => {
        f[k].value = undefined
      })
      return { ...f };
    });
    // console.log("Filtry cleared")

    isLoading.set(true);
    await goto(`/${url}?` + params, { replaceState: false, keepFocus: true, noScroll: true });
    isLoading.set(false);
  }

  function updateFilterByName(name: string, value: unknown) {
    filters.update((f) => {
      if (f[name]) f[name].value = value;
      return { ...f };
    });
  }

  function updateFilterTypeByName(name: string, value: FilterType) {
    filters.update((f) => {
      if (f[name]) f[name].type = value;
      return { ...f };
    });
  }

 

  return {
    pagination,
    sorting,
    filters,
    isLoading,
    queryData,
    queryDataAfterPageChange,
    resetFilters,
    updateFilterByName,
    updateFilterTypeByName,
  };
}


