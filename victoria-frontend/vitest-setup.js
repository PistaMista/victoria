import '@testing-library/jest-dom/vitest'
import { beforeAll, afterAll, afterEach } from 'vitest'
import { server } from './src/mocks/node'

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())