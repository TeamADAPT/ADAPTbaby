## Quickstart

Whisper Large v3 Turbo is now available. [Learn more](https://groq.com/whisper-large-v3-turbo-now-available-on-groq-combining-speed-quality-for-speech-recognition/).

Get up and running with the Groq API in a few minutes.

### [Create an API Key](https://console.groq.com/docs/quickstart#create-an-api-key)

Please visit [here](https://console.groq.com/keys) to create an API Key.

### [Set up your API Key (recommended)](https://console.groq.com/docs/quickstart#set-up-your-api-key-recommended)

Configure your API key as an environment variable. This approach streamlines your API usage by eliminating the need to include your API key in each request. Moreover, it enhances security by minimizing the risk of inadvertently including your API key in your codebase.

#### In your terminal of choice:

```shell
export GROQ_API_KEY=<your-api-key-here>
```

### [Requesting your first chat completion](https://console.groq.com/docs/quickstart#requesting-your-first-chat-completion)

#### Pass the following as the request body:

```json
{ "messages": [ { "role": "user", "content": "Explain the importance of fast language models" } ], "model": "mixtral-8x7b-32768" }
```

Now that you have successfully received a chat completion, you can try out the other endpoints in the API.

### [Next Steps](https://console.groq.com/docs/quickstart#next-steps)

-   Check out the [Playground](https://console.groq.com/playground) to try out the Groq API in your browser
-   Join our GroqCloud developer community on [Discord](https://discord.gg/groq)
-   [Chat with our Docs](https://docs-chat.groqcloud.com/) at lightning speed using the Groq API!
-   Add a how-to on your project to the [Groq API Cookbook](https://github.com/groq/groq-api-cookbook)