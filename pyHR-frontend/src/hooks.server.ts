
import { redirect, type Handle, type HandleFetch } from '@sveltejs/kit';
import { API_URL } from '$env/static/private';
import { COOKIE_AUTH_NAME } from '$lib';

export const handle : Handle = async ({ event , resolve })  => {

	const authCookie = event.cookies.get(COOKIE_AUTH_NAME);
	if (!event.url.pathname.endsWith("login") && !authCookie) {
		redirect(303, "/login")
	}

	return await resolve(event);
}

export const handleFetch: HandleFetch = async({event, request, fetch}) => {
	if (request.url.startsWith(API_URL)) {
		request.headers.set("Accept-Language", "pl")
		const authCookie = event.cookies.get(COOKIE_AUTH_NAME);
		if (authCookie) {
			request.headers.set('Authorization', `Bearer ${authCookie}`)
		}
		if (!event.url.pathname.endsWith("login")) {
			const res = await fetch(request);
			if (res.status === 401) {
				event.cookies.delete(COOKIE_AUTH_NAME, {path: "/"});
				redirect(303, "/login");
			}
			return res
		}
	}
	


	return fetch(request);
}
