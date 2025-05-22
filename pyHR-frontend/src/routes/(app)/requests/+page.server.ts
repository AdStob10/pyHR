import { API_URL } from "$env/static/private";
import { addRequestSchema,   type AddRequestSchema } from "$lib/components/custom/Forms/schema";
import type { VacationRequest } from "$lib/types";
import { flattenVacationRequest } from "$lib/utils/objects";
import type { Actions } from "@sveltejs/kit";
import { fail, message, superValidate, type Infer } from "sveltekit-superforms";
import { zod } from "sveltekit-superforms/adapters";

export const actions: Actions = {
  default: async (event) => {
    const form = await superValidate<Infer<AddRequestSchema>>(event, zod(addRequestSchema));

    if (!form.valid) {
      return fail(400, {
        form,
      });
    }
    try {
      const { data } = form
      const flatData = flattenVacationRequest(data)
      const res = await event.fetch(`${API_URL}/vacation/add`, {
        method: "POST",
        body: JSON.stringify(flatData),
        headers: {
        'Content-Type': 'application/json'
        }
      })
      
      console.log("data", flatData)

      if (res.status == 422 ) {
        const text = await res.text()
        console.error(text)
        return message(form, {status: "error", text: "Niepoprawne dane"}, {status: 422} )
      }

      if (res.status == 400 || res.status == 404) {
        const responseData = await res.json()
        console.error(responseData)
        return message(form, {status: "error", text: responseData.detail}, {status: res.status})
      }

      const bodyResponse: VacationRequest  = await res.json()
      return message(form, {status:"success", text:`Dodano wniosek o numerze ${bodyResponse.id}`})

    } catch (e) {
      console.error(e)
      return message(form, {status: "error", text:"Błąd przy próbie dodania wniosku"}, {status: 400})
    }

    
  },
};