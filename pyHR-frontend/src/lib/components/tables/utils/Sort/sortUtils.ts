import type { ColumnSort, SortingState } from "@tanstack/table-core"

function convertCamelToSnake(str: string){
 return str.replace(/([a-zA-Z])(?=[A-Z])/g,'$1_').toLowerCase()
}

export const setSortingOnParams = (sorts: SortingState, params: URLSearchParams) => {
    sorts.forEach((s: ColumnSort) => {
        params.set(`sort_${convertCamelToSnake(s.id)}`, s.desc ? "DESC" : "ASC")
    })
    return params
}

