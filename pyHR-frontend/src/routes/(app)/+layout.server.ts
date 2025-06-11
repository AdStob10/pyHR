import { env } from '$env/dynamic/private';
import type { UserData, UserWithRole } from "$lib/types";
import { availableRoles } from "$lib/utils/objects";
import type { LayoutServerLoad } from "../(app)/$types";


export const load: LayoutServerLoad = async ({fetch}) => {
    const data: UserData = await (await fetch(`${env.API_URL}/login/info`)).json()
    const role = availableRoles.find(ar => ar.id == data.role)
    const user = {...data, role}

    return {
        user
    } as {user: UserWithRole}
};