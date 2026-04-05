import { ws } from "msw";
import { spy } from "../spy";

const socket = ws.link("ws:/websocket")


export const connectionHandler = await spy(() => {
});

export const disconnectionHandler = await spy(() => {
});


export const handlers = [
	socket.addEventListener('connection', connectionHandler)
];

