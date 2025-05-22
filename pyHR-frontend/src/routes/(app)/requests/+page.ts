import type { PaginatedList, VacationRequest } from "$lib/types";
import { superValidate, type Infer, type SuperValidated } from "sveltekit-superforms";
import type { PageLoad} from "./$types";
import { zod } from "sveltekit-superforms/adapters";
import { addRequestSchema, type AddRequestSchema } from '$lib/components/custom/Forms/schema';


export const load: PageLoad = async ({fetch, url}) => {
    const apiUrl = `/api/vacation/requests?${url.searchParams}`;
    const response = await fetch(apiUrl)
    const data = await response.json()
    const form = await superValidate(zod(addRequestSchema))
    return {
        vacations: data,
        form,
    } as {vacations: PaginatedList<VacationRequest>, form: SuperValidated<Infer<AddRequestSchema>>}
};
