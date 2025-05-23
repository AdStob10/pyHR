import { API_URL } from "$env/static/private";
import type { VacationType } from "$lib/types";
import type { LayoutServerLoad } from "./$types";



export const load: LayoutServerLoad = async ({fetch}) => {
    const data = await (await fetch(`${API_URL}/vacation/types`)).json()
    return {
        vacationTypes: data,

    } as {vacationTypes: VacationType[]}
};
