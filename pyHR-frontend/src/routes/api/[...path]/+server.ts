import { env } from '$env/dynamic/private';
import type { RequestHandler } from './$types';


export const GET: RequestHandler = ({ params, url, fetch}) => {
    // console.log("proxy", params.path)
	return fetch(`${env.API_URL}/${params.path + url.search}`);
};

export const POST: RequestHandler = ({ params, url, request, fetch}) => {
    // console.log("proxy post", params.path)
	return fetch(`${env.API_URL}/${params.path + url.search}`, request);
};