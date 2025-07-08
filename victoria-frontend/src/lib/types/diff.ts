export type Diff<T> = {
    [K in keyof T]: T[K] | undefined;
}

// FIXME: This will not work with nested objects
export function getDiff<T extends object>(oldObj: T, newObj: T): Diff<T> {
    const result = {} as Diff<T>;
    
    Object.keys(oldObj).forEach((key) => {
        const valNew = newObj[key as keyof T];
        const valOld = oldObj[key as keyof T];

        if (valNew !== valOld) {
            result[key as keyof T] = valNew;
        }
    })
    
    return result;
}