import { API_URL } from "$env/static/private";
import type { UserData } from "$lib/types";
import type { PageServerLoad } from "../login/$types";

export const load: PageServerLoad = async ({fetch}) => {
    const data = await (await fetch(`${API_URL}/login/info`)).json()
    console.log(data)
    return {
        user: fetch(`${API_URL}/login/info`).then(r => r.json())
    } as {user: Promise<UserData>}
};