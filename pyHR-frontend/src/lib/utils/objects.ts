import type { AddRequestSchema } from "$lib/components/custom/Forms/schema";
import { Circle, CircleCheckBig, CircleOff,  } from "@lucide/svelte";
import type { Component } from "svelte";
import type { Infer } from "sveltekit-superforms";


/********* Statuses utils *********/

export type VacationStatus = {
    id: number,
    name: string,
    icon: Component
}

export const vacationStatuses: VacationStatus[] = [
    {
        id: 0,
        name: "Nowy",
        icon: Circle
    },
    {
        id: 1,
        name: "Zaakceptowany",
        icon: CircleCheckBig
    },
    {
        id: 2,
        name: "Odrzucony",
        icon: CircleOff
    }
]


export const statutesAsOptions = () => {
    return vacationStatuses.map(status => ({label: status.name, value: status.id, icon: status.icon}))
} 

/********* Role utils *********/

export type Role = {
    id: number,
    name: string,
    label: string,
}


export const availableRoles: Role[] = [
    {
        id: 0,
        name: "BASIC_EMPLOYEE",
        label: "Pracownik"
    },
    {
        id: 1,
        name: "MANAGER",
        label: "Kierownik",    
    },
    {
        id: 3,
        name: "ADMIM",
        label: "Administrator"
    }
]



/********* Request utils *********/


export const flattenVacationRequest = (obj: Infer<AddRequestSchema>) => ({
    reason: obj.reason,
    vacationTypeId: obj.vacationTypeId,
    startDate: obj.dateRange.startDate,
    endDate: obj.dateRange.endDate
})



export const getVacationDuration = (start: string, end: string) => {
    const startDate = new Date(start)
    const endDate = new Date(end)
    const oneDay = 24 * 60 * 60 * 1000; 
    const diffInMilliseconds = endDate.getTime() - startDate.getTime();
    const diffInDays = Math.round(diffInMilliseconds / oneDay);
    
    if (diffInDays == 0) return 1
    return diffInDays + 1
}