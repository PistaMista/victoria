export async function getQueryAnswer(id: number): Promise<any> {
	const res = await fetch(`/api/queries/${id}/answer`, {
		method: "GET",
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return json;
}

export async function sendQueryAnswer(id: number, answer: any): Promise<any> {
	const res = await fetch(`/api/queries/${id}/answer`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(answer),
	});
	const json = await res.json();

	if (!res.ok) {
		throw Error(json.detail);
	}

	return json;
}
