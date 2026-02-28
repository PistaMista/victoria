export async function spy<T extends (...args: any[]) => any>(
  implementation: T,
): Promise<T | ReturnType<typeof vi.fn>> {
  let isBrowser = typeof process === "undefined";
  if (isBrowser) {
    return implementation;
  } else {
    let vi = (await import("vitest"))["vi"];
    return vi.fn(implementation);
  }
}
