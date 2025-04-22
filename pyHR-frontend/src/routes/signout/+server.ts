import { COOKIE_AUTH_NAME } from "$lib";
import { redirect, type RequestHandler } from "@sveltejs/kit";



export const GET: RequestHandler = async ({cookies}) => {
    cookies.delete(COOKIE_AUTH_NAME, {path: "/"})
    return redirect(307, "/login")
};