import { env } from '$env/dynamic/private';
import type { AvailableVacation, VacationType } from "$lib/types";
import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async ({fetch, depends}) => {

    depends("app:request:layout")
    const data = await (await fetch(`${env.API_URL}/vacation/types`)).json()
    const availableDays = await (await fetch(`${env.API_URL}/vacation/available`)).json()
    return {
        vacationTypes: data,
        availableDays
    } as {vacationTypes: VacationType[], availableDays: AvailableVacation[]}
};