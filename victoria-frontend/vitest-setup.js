import "@testing-library/jest-dom/vitest";
import { beforeAll, afterAll, beforeEach, afterEach } from "vitest";
import { server } from "./src/mocks/node";
import { Settings, IANAZone } from "ts-luxon";
import { resetStores } from "$lib/stores/stores";

beforeAll(() => server.listen());
beforeEach(() => (Settings.defaultZone = IANAZone.create("UTC")));
afterEach(() => {
  server.resetHandlers();
  resetStores();
});
afterAll(() => server.close());
