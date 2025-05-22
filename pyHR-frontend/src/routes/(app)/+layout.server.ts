import { API_URL } from "$env/static/private";
import type { UserData } from "$lib/types";
import type { LayoutServerLoad } from "../(app)/$types";


export const load: LayoutServerLoad = async ({fetch}) => {
    const data = await (await fetch(`${API_URL}/login/info`)).json()
    console.log(data)
    return {
        user: fetch(`${API_URL}/login/info`).then(r => r.json())
    } as {user: Promise<UserData>}
};