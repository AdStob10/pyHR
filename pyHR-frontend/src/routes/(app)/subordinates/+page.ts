import { redirect } from "@sveltejs/kit";
import type { PageLoad } from "./$types";
import type { PaginatedList, EmployeeDetails } from "$lib/types";

export const load: PageLoad = async ({fetch, parent, url, depends}) => {
    const parentData = await parent();
    if (parentData.user.role.name === "BASIC_EMPLOYEE") {
        redirect(303, "/")
    }


    const apiUrl = `/api/employee/all?${url.searchParams}`;
    const response = await fetch(apiUrl)
    if (response.status == 401) {
        redirect(303, "/signout")
    }

    const data = await response.json()
    depends("app:subordinates")


    return {
        employees: data
    } as {employees: PaginatedList<EmployeeDetails>};

};