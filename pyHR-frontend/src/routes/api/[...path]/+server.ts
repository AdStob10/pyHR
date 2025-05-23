import { API_URL } from '$env/static/private';
import type { RequestHandler } from './$types';


export const GET: RequestHandler = ({ params, url, fetch}) => {
    console.log("proxy", params.path)
	return fetch(`${API_URL}/${params.path + url.search}`);
};

export const POST: RequestHandler = ({ params, url, request, fetch}) => {
    console.log("proxy post", params.path)
	return fetch(`${API_URL}/${params.path + url.search}`, request);
};