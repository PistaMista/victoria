import { http, HttpResponse, delay } from "msw";
import { Exchange } from "$lib/types/exchange";
import { Message } from "$lib/types/message";
import { spy } from "../spy";

export const getMessagesHandler = await spy(async ({ request }) => {
	let url: URL = new URL(request.url);
	let after: number = Number(url.searchParams.get("after"));

	await delay(400);

	if (after < 5000) {
		return HttpResponse.json<Message[]>([
			{
				id: 2,
				timestamp: 5000,
				senderName: "Researcher",
				content: {
					type: "markdown",
					markdownText: `
Agent message!

Furthermore here is some very long text to test out the margins and formatting of this message element. If it looks bizzarre in anyway, that is wrong. It must look good. This is a professional application made by a rather professional person. This text must be absolutely perfect in every single way an earthly creature might conceive of. 

# h1 Heading 8-)
## h2 Heading
### h3 Heading
#### h4 Heading
##### h5 Heading
###### h6 Heading

## Horizontal Rules

___

---

***
## Emphasis

**This is bold text**

__This is bold text__

*This is italic text*

_This is italic text_

~~Strikethrough~~

## Lists

Unordered

+ Create a list by starting a line with \`+\`, \`-\`, or \`*\`
+ Sub-lists are made by indenting 2 spaces:
  - Marker character change forces new list start:
    * Ac tristique libero volutpat at
    + Facilisis in pretium nisl aliquet
    - Nulla volutpat aliquam velit
+ Very easy!

Ordered

1. Lorem ipsum dolor sit amet
2. Consectetur adipiscing elit
3. Integer molestie lorem at massa


1. You can use sequential numbers...
1. ...or keep all the numbers as

## Tables

| Option | Description |
| ------ | ----------- |
| data   | path to data files to supply the data that will be passed into templates. |
| engine | engine to be used for processing templates. Handlebars is the default. |
| ext    | extension to be used for dest files. |

Right aligned columns

| Option | Description |
| ------:| -----------:|
| data   | path to data files to supply the data that will be passed into templates. |
| engine | engine to be used for processing templates. Handlebars is the default. |
| ext    | extension to be used for dest files. |

## Images

![Minion](https://octodex.github.com/images/minion.png)
![Stormtroopocat](https://octodex.github.com/images/stormtroopocat.jpg "The Stormtroopocat")
					`,
				},
			},
		]);
	} else if (after < 7000) {
		return HttpResponse.json<Message[]>([
			{
				id: 3,
				timestamp: 6500,
				senderName: "Cook",
				content: {
					type: "choice_prompt",
					prompt: "Pick a thing",
					queryId: 1,
					choices: [{ value: "lol" }],
				},
			},
			{
				id: 4,
				timestamp: 7000,
				senderName: "John",
				content: {
					type: "action_confirmation",
					invocationThought: {
						type: "ActionInvocation",
						name: "add_to_calendar",
						parameters: {
							date: "20",
							delete: true,
						},
					},
					queryId: 2,
				},
			},
		]);
	} else if (after < 9000) {
		return HttpResponse.json<Message[]>([
			{
				id: 3,
				timestamp: 9000,
				senderName: "Gustave",
				content: {
					type: "image",
					imageDataURI: "data/png;asdakwdkjn",
				},
			},
		]);
	} else {
		return HttpResponse.json<Message[]>([]);
	}
});

export const handlers = [
	// This is an HTTP long poll for agent messages sent after a given timestamp
	http.get("/api/exchanges/:id/messages", getMessagesHandler),
];
