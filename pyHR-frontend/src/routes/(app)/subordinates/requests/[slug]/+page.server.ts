import { API_URL } from "$env/static/private";
import type { PageServerLoad } from "./$types";
import type { SubordinateVacationRequest} from "$lib/types";
import { error } from "@sveltejs/kit";



export const load: PageServerLoad = async ({params, fetch, depends}) => {
    const res = await fetch(`${API_URL}/vacation/employees/${params.slug}`)
    if (res.status !== 200) {
        error(404, "Nie znaleziono takiego wniosku urlopowego :)")
    }

    depends("app:sub:emp:request")
    const data = await res.json()
    return {
        vacation:  data
    } as {vacation: SubordinateVacationRequest}
};