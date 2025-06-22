import type { EmployeeDetailsWithManager } from "$lib/types";
import type { PageLoad } from "./$types";
import { error } from "@sveltejs/kit";

export const load: PageLoad = async ({params, parent, fetch}) => {
    const parentData = await parent();
    let res
    if (parentData.user.role.name === "BASIC_EMPLOYEE" || parentData.user.id == Number.parseInt(params.slug)) {
        res = await fetch(`/api/employee/details`)
    }
    else {
        res = await fetch(`/api/employee/details/${params.slug}`)
    }
    if (res.status !== 200) {
        error(404, "Nie znaleziono takiego pracownika :)")
    }


    return {
        employee:  await res.json()
    } as {employee: EmployeeDetailsWithManager}
};