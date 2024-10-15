#### Install the Groq JavaScript library:

```shell
npm install --save groq-sdk
```

#### Performing a Chat Completion:

```js
1import Groq from "groq-sdk"; 2 3const groq = new Groq({ apiKey: process.env.GROQ_API_KEY }); 4 5export async function main() { 6 const chatCompletion = await getGroqChatCompletion(); 7 // Print the completion returned by the LLM. 8 console.log(chatCompletion.choices[0]?.message?.content || ""); 9} 10 11export async function getGroqChatCompletion() { 12 return groq.chat.completions.create({ 13 messages: [ 14 { 15 role: "user", 16 content: "Explain the importance of fast language models", 17 }, 18 ], 19 model: "llama3-8b-8192", 20 }); 21}
```