import { authToken } from "./auth";

export function resetStores() {
    authToken.set(null);
}