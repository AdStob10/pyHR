import { API_URL } from "$env/static/private";
import type { PageServerLoad } from "./$types";
import type { VacationRequest } from "$lib/types";
import { error } from "@sveltejs/kit";



export const load: PageServerLoad = async ({params, fetch}) => {
    const res = await fetch(`${API_URL}/vacation/requests/${params.slug}`)
    if (res.status !== 200) {
        error(404, "Nie znaleziono takiego wniosku urlopowego :)")
    }

    return {
        vacation:  await res.json()
    } as {vacation: Promise<VacationRequest>}
};