# ✅ Install required packages
!pip install -q openai gradio

# ✅ Imports
from openai import OpenAI
import gradio as gr
import os

# ✅ Load API key from Hugging Face Secrets
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("⚠️ OPENROUTER_API_KEY not found. Add it in HF Spaces > Settings > Secrets.")

# ✅ OpenRouter API client setup
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# ✅ Chat function using Kimi-K2
def ask_kimi(prompt, history=[]):
    messages = [{"role": "system", "content": "Wewe ni msaidizi mzuri wa kujifunza programu kwa Kiswahili."}]
    for user, bot in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": bot})
    messages.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model="moonshotai/kimi-k2:free",
        messages=messages,
        extra_headers={
            "HTTP-Referer": "https://your-site.com",
            "X-Title": "NextDev Academy",
        }
    )

    reply = completion.choices[0].message.content
    history.append((prompt, reply))
    return reply, history

# ✅ Gradio UI with submit button
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 Kimi K2 Chatbot kwa Kiswahili (Powered by OpenRouter)")

    chatbot = gr.Chatbot()
    state = gr.State([])

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Uliza swali kuhusu programu au teknolojia...",
            show_label=False,
            scale=4
        )
        submit = gr.Button("➡️ Tuma", scale=1)

    clear = gr.Button("🔄 Anza upya")

    # Chat submission logic
    def user_submit(user_message, history):
        response, updated_history = ask_kimi(user_message, history)
        return updated_history, updated_history

    msg.submit(user_submit, [msg, state], [chatbot, state])
    submit.click(user_submit, [msg, state], [chatbot, state])

    clear.click(lambda: ([], []), None, [chatbot, state])

demo.launch(css="custom.css")

