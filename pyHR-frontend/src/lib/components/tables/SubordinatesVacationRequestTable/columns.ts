import { renderComponent } from "$lib/components/ui/data-table";
import type { SubordinateVacationRequest } from "$lib/types";
import type { ColumnDef } from "@tanstack/table-core";
import StatusCell from "../utils/StatusCell/StatusCell.svelte";
import SortHeader from "../utils/Sort/SortHeader.svelte";
import SubVacationRequestsActions from "./SubVacationRequestsActions.svelte";

export const columns: ColumnDef<SubordinateVacationRequest>[] = [
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
        header:"Pracownik",
        accessorFn: row => `${row.employee.firstName} ${row.employee.lastName}`
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
        accessorKey:"status",
        header:"Status",
        cell: ({row}) => {
            return renderComponent(StatusCell, {statusId: row.original.status})
        }

    },
    {
        id: "actions",
        cell: ({ row }) => {
           return renderComponent(SubVacationRequestsActions, { id: row.getValue("id") as number, statusId: row.getValue("status") as number });
        }
    }
]; 