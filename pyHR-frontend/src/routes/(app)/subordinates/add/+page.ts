import { redirect } from "@sveltejs/kit";
import type { PageLoad } from "./$types";
import { superValidate, type Infer, type SuperValidated } from "sveltekit-superforms";
import { addEmployeeSchema, type AddEmployeeSchema} from '$lib/components/custom/Forms/AddEmployee/schema';
import { zod } from "sveltekit-superforms/adapters";

export const load: PageLoad = async ({parent}) => {
    const parentData = await parent();
    if (parentData.user.role.name === "BASIC_EMPLOYEE") {
        redirect(303, "/")
    }

    const form = await superValidate(zod(addEmployeeSchema))
    return {
        form
    } as {form: SuperValidated<Infer<AddEmployeeSchema>>}

};