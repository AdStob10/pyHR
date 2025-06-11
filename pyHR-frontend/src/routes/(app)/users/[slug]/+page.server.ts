import { env } from '$env/dynamic/private';
import type { EmployeeDetailsWithManager } from "$lib/types";
import type { PageServerLoad } from "./$types";
import { error } from "@sveltejs/kit";

export const load: PageServerLoad = async ({params, parent, fetch}) => {
    const parentData = await parent();
    let res
    if (parentData.user.role.name === "BASIC_EMPLOYEE" || parentData.user.id == Number.parseInt(params.slug)) {
        res = await fetch(`${env.API_URL}/employee/details`)
    }
    else {
        res = await fetch(`${env.API_URL}/employee/details/${params.slug}`)
    }
    if (res.status !== 200) {
        error(404, "Nie znaleziono takiego pracownika :)")
    }

    const data = await res.json()
    // console.log(data)
    return {
        employee:  data
    } as {employee: EmployeeDetailsWithManager}
};