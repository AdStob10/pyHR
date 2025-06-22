import { redirect } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({parent}) => {
    const parentData = await parent();
    if (parentData.user.role.name === "BASIC_EMPLOYEE") {
        redirect(303, "/")
    }
    
    redirect(303, "/subordinates")
};