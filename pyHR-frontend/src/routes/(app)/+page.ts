import type { AvailableVacation, VacationInMonth, VacationType } from "$lib/types";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({fetch}) => {
    const vacationTypes = await (await fetch(`api/vacation/types`)).json()
    const availableDays = await (await fetch(`api/vacation/available`)).json()
    const vacationInMonth = await (await fetch("api/vacation/report/months")).json()
    return {
        vacationTypes,
        availableDays,
        vacationInMonth,
    } as {vacationTypes: VacationType[] ,availableDays: AvailableVacation[], vacationInMonth: VacationInMonth[]}
};