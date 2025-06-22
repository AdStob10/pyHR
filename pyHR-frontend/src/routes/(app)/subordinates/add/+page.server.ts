import { env } from '$env/dynamic/private';
import { addEmployeeSchema, type AddEmployeeSchema } from "$lib/components/custom/Forms/AddEmployee/schema";
import type { EmployeeDetails } from "$lib/types";
import type { Actions } from "@sveltejs/kit";
import { fail, message, superValidate, type Infer } from "sveltekit-superforms";
import { zod } from "sveltekit-superforms/adapters";

export const actions: Actions = {
  default: async (event) => {
    const form = await superValidate<Infer<AddEmployeeSchema>>(event, zod(addEmployeeSchema));

    if (!form.valid) {
      return fail(400, {
        form,
      });
    }
    try {
      const { data } = form;
      const res = await event.fetch(`${env.API_URL}/employee/create`, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
        'Content-Type': 'application/json'
        }
      })
      
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

      const bodyResponse: EmployeeDetails  = await res.json()
      return message(form, {status:"success", text:`Dodano użytkownika o numerze ${bodyResponse.id}`})

    } catch (e) {
      console.error(e)
      return message(form, {status: "error", text:"Błąd przy próbie dodania wniosku"}, {status: 400})
    }

    
  },
};

