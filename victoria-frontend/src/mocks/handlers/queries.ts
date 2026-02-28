import { http, HttpResponse } from "msw";
import { spy } from "../spy";

export const getQueryAnswerHandler = await spy(({ params: { id } }) => {
  switch (id) {
    case "1":
      return HttpResponse.json<any>(true);
    case "2":
      return HttpResponse.json<any>(false);
    case "3":
      return HttpResponse.json<any>(null);
    case "4":
      return HttpResponse.json<any>([1, 2, 3]);
    case "5":
      return HttpResponse.json<any>("blue");
    default:
      return HttpResponse.json<any>(null, { status: 404 });
  }
});

export const answerQueryHandler = await spy(({ params: { id } }) => {
  switch (id) {
    case "3":
      return HttpResponse.json<any>(true);
    case "1":
    case "2":
    case "4":
    case "5":
      return HttpResponse.json<any>(
        { error: "Already answered" },
        { status: 400 },
      );
    default:
      return HttpResponse.json<any>(null, { status: 404 });
  }
});

export const handlers = [
  http.get("/api/queries/:id/answer", getQueryAnswerHandler),
  http.post("/api/queries/:id/answer", answerQueryHandler),
];
