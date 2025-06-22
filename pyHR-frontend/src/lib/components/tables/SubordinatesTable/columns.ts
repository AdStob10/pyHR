import { renderComponent } from "$lib/components/ui/data-table";
import type { EmployeeDetails } from "$lib/types";
import type { ColumnDef } from "@tanstack/table-core";
import SortHeader from "../utils/Sort/SortHeader.svelte";


export const columns: ColumnDef<EmployeeDetails>[] = [
     {
        accessorKey: "id",
        header: ({column}) => {
            return renderComponent(SortHeader, 
                {
                    label: "ID", 
                    direction: column.getIsSorted(),
                    onclick: column.getToggleSortingHandler()
                })
        }
    },
    {
        accessorKey:"fullName",
        header: ({column}) => {
            return renderComponent(SortHeader, 
                {
                    label: "Imię i nazwisko", 
                    direction: column.getIsSorted(),
                    onclick: column.getToggleSortingHandler()
                })
        }
    },
    {
        accessorKey:"employmentDate",
        header: ({column}) => {
            return renderComponent(SortHeader, 
                {
                    label: "Data zatrudnienia", 
                    direction: column.getIsSorted(),
                    onclick: column.getToggleSortingHandler()
                })
        }
    },
    {
        header:"Stanowisko",
        accessorKey:"jobTitle",
    },
    {
        header:"Dział",
        accessorKey:"department",
    }
]