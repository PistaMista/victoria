export class Deferred<T> {
	public readonly promise: Promise<T>;
	private _resolve!: (val: T | PromiseLike<T>) => void;
	private _reject!: (reason?: any) => void;

	constructor() {
		this.promise = new Promise((resolve, reject) => {
			this._resolve = resolve;
			this._reject = reject;
		});
	}

	public resolve(value: T | PromiseLike<T>): void {
		this._resolve(value);
	}

	public reject(reason?: any): void {
		this._reject(reason);
	}
};


