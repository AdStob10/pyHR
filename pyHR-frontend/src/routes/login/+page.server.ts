import { API_URL } from '$env/static/private';
import { COOKIE_AUTH_NAME } from '$lib';
import { authFormSchema, type AuthFormSchema } from '$lib/components/custom/AuthForm/schema';
import type { TokenData } from "$lib/types";
import { redirect } from '@sveltejs/kit';
import type { JwtPayload } from 'jwt-decode';
import { jwtDecode } from 'jwt-decode';
import { fail, message, superValidate, type Infer } from 'sveltekit-superforms';
import { zod } from "sveltekit-superforms/adapters";
import type { Actions, PageServerLoad } from './$types';

const TOLERANCE = 3 * 60;

export const load: PageServerLoad = async ({cookies}) => {
    
    if (cookies.get(COOKIE_AUTH_NAME)) redirect(303, "/")

    return {
        form: await superValidate(zod(authFormSchema))
    }
};


export const actions: Actions = {
    default: async ({request, cookies, fetch}) => {
        const formData = await request.formData();
        const form = await superValidate<Infer<AuthFormSchema>>(formData, zod(authFormSchema));
        if (!form.valid) {
            return fail(400, {
                form
            });
        }

        const res = await fetch(`${API_URL}/login/access-token`, {
            method: "POST",
            body: formData
        })

        if (res.status === 401) {
            return message(form, {status: "error", text:"Niepoprawny login lub hasło"}, {status: 401})
        }
        
        console.log(res)
        const tokenData: TokenData = await res.json();
      
        const decoded = jwtDecode<JwtPayload>(tokenData.access_token);
        if (!decoded.exp) {
            throw new Error("Missing expiring information in token");
        }

        const nowInSeconds = Math.floor(Date.now() / 1000)
        const maxAge = decoded.exp  - nowInSeconds - TOLERANCE; 
        cookies.set("pyhr_auth", tokenData.access_token, {path: "/", maxAge})

        return redirect(303, "/")
    }
};