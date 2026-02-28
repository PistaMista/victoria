import { delay, http, HttpResponse } from "msw";
import { spy } from "../spy";

export const loginHandler = await spy(async ({ request }) => {
  let body = await request.clone().json();

  if (body.username === "tester" && body.password === "lolec") {
    return HttpResponse.json(
      {},
      {
        headers: {
          "Set-Cookie": "token=jwt-token; Path=/; HttpOnly; Max-Age=3600",
        },
      },
    );
  } else {
    return HttpResponse.json(
      {
        error: "Invalid credentials",
      },
      { status: 401 },
    );
  }
});

export const registerHandler = await spy(async () => {
  return HttpResponse.json({});
});

export const handlers = [
  http.post("/api/auth/login", loginHandler),
  http.post("/api/auth/register", registerHandler),
];
