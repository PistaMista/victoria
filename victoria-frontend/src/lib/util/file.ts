export function convertToDataURI(file: File): Promise<string> {
	return new Promise((resolve, reject) => {
		const reader = new FileReader();
		reader.onload = () => {
			const result = reader.result;

			if (typeof result === "string") {
				resolve(result);
			} else {
				reject(new Error("FileReader result is not a string"));
			}
		};

		reader.onerror = () => reject(reader.error);

		reader.readAsDataURL(file);
	});
}
