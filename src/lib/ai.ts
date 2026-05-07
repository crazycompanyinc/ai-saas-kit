import OpenAI from "openai"

let _openai: OpenAI | null = null

export function getOpenAI(): OpenAI {
  if (!_openai) {
    _openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY || "placeholder",
    })
  }
  return _openai
}

export async function streamChat(
  messages: { role: "user" | "system" | "assistant"; content: string }[]
) {
  const openai = getOpenAI()
  const response = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: messages as any,
    stream: false,
  })
  return response.choices[0].message.content
}
