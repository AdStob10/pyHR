import { renderComponent } from "$lib/components/ui/data-table";
import type { VacationRequest } from "$lib/types";
import type { ColumnDef } from "@tanstack/table-core";
import StatusCell from "../utils/StatusCell/StatusCell.svelte";
import SortHeader from "../utils/Sort/SortHeader.svelte";
import { getVacationDuration } from "$lib/utils/objects";

export const columns: ColumnDef<VacationRequest>[] = [
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
        accessorKey:"startDate",
        header: ({column}) => {
            return renderComponent(SortHeader, 
                {
                    label: "Początek", 
                    direction: column.getIsSorted(),
                    onclick: column.getToggleSortingHandler()
                })
        }
    },
    {
        accessorKey:"endDate",
        header: ({column}) => {
            return renderComponent(SortHeader, 
                {
                    label: "Koniec", 
                    direction: column.getIsSorted(),
                    onclick: column.getToggleSortingHandler()
                })
        }
    },
    {
        header:"Ilość dni",
        accessorFn: row => getVacationDuration(row.startDate, row.endDate)
    },
    {
        accessorKey:"status",
        header:"Status",
        cell: ({row}) => {
            return renderComponent(StatusCell, {statusId: row.getValue("status")})
        }

    },
    {
        accessorKey:"vacationType.name",
        header:"Rodzaj urlopu"
    }
]; 