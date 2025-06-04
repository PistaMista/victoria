if (import.meta.env.DEV) {
    const { worker } = await import('./mocks/browser');
    worker.start();
}