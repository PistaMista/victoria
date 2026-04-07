import "@testing-library/jest-dom/vitest";
import { beforeAll, afterAll, beforeEach, afterEach } from "vitest";
import { server } from "./src/mocks/node";
import { Settings, IANAZone } from "ts-luxon";
import { resetStores } from "$lib/stores/stores";
import { connectWithRetry, disconnect } from "$lib/api/websocket";

beforeAll(() => {
	server.listen();
	connectWithRetry(); // Connect main websocket
});
beforeEach(() => (Settings.defaultZone = IANAZone.create("UTC")));
afterEach(() => {
	server.resetHandlers();
	resetStores();
});
afterAll(() => {
	disconnect(); // Disconnect main websocket
	server.close();
});
