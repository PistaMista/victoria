export type Diff<T> = {
    [K in keyof T]: 
        T[K] extends any[] ? T[K] | undefined :
        T[K] extends object ? Diff<T[K]> | undefined :
        T[K] | undefined;
}

export function getDiff<T extends object>(oldObj: T, newObj: T): Diff<T> {
    const result = {} as Diff<T>;
    
    Object.keys(oldObj)
    .concat(Object.keys(newObj))
    .forEach((k) => {
        const key = k as keyof T;
        const valNew = newObj[key];
        const valOld = oldObj[key];

        // Arrays
        if (Array.isArray(valNew) && Array.isArray(valOld)) {
            if (valNew.some((v, i) => v !== valOld[i])) {
                result[key] = structuredClone(valNew);
            }
        // Plain objects
        } else if (
            typeof valOld === 'object' && typeof valNew === 'object'
            && valOld !== null && valNew !== null
        ) {
            const diff = getDiff(valOld, valNew);
            if (Object.keys(diff).length > 0) {
                result[key] = structuredClone(diff) as any;
            }
        // Primitives
        } else if (valNew !== valOld) {
            result[key] = valNew;
        }
    })
    
    return result;
}