import { API_URL } from '$env/static/private';
import type { RequestHandler } from './$types';


export const GET: RequestHandler = ({ params, url, fetch}) => {
    console.log("proxy", params.path)
	return fetch(`${API_URL}/${params.path + url.search}`);
};