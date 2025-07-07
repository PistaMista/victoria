import '@testing-library/jest-dom/vitest'
import { beforeAll, afterAll, beforeEach, afterEach } from 'vitest'
import { server } from './src/mocks/node'
import { Settings, IANAZone } from 'ts-luxon'

beforeAll(() => server.listen())
beforeEach(() => Settings.defaultZone = IANAZone.create('UTC'))
afterEach(() => { 
    server.resetHandlers();
})
afterAll(() => server.close())