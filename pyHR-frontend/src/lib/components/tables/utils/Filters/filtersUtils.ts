import type { SelectOption } from "$lib/components/custom/SelectWrapper/SelectWrapper.svelte"


type FilterType = 'eq' | 'ge' | 'le' | 'gt' | 'lt'



type FilterItem = {
    label?: string,
    name: string,
    value: unknown
    type?: FilterType
}


const filterTypesDate: SelectOption[] = [
    {
        label: "Od",
        value: "ge",
        icon: undefined
    },
    {
        label: "Do",
        value: "le",
        icon: undefined
    },
    {
        label: "Równy",
        value: "eq",
        icon: undefined
    },
]


const setFiltersOnParams = (filters: Record<string, FilterItem>, params: URLSearchParams) => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    Object.entries(filters).forEach(([_, filter]) => {
        if (filter.value !== undefined && filter.value !== null) {
            if (filter.type) {
                params.set(`${filter.name}_${filter.type}`, filter.value.toString())
            } else {
                params.set(filter.name, filter.value.toString())
            }
        }
    })
    return params
}



export { filterTypesDate as filterTypes, setFiltersOnParams, type FilterItem, type FilterType }

