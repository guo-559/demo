import gradio as gr
from openai import OpenAI

class Conversation:
    def __init__(self):
        self.history = [("system", "You are a helpful assistant")]
        self.client = OpenAI(base_url="http://10.254.50.50:8001/v1", api_key="not-used")

    def predict(self, prompt, state):
        if state is None:
            state = self.history.copy()

        user_message = ("user", prompt)
        state.append(user_message)

        try:
            response = self.client.chat.completions.create(
                model="meta/llama3-8b-instruct",
                max_tokens=2000,
                stream=True,
                temperature=0.4,
                messages=[{"role": role, "content": content} for role, content in state],
                top_p=0.3
            )

            partial_msg = ""

            for chunk in response:
                if hasattr(chunk, 'choices') and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                    partial_msg += chunk.choices[0].delta.content

                    # Debug print to inspect what is being yielded
                    print("Yielding:", state + [("assistant", partial_msg)])

                    yield state + [("assistant", partial_msg)]

            state.append(("assistant", partial_msg))
        except Exception as e:
            # Handle exceptions
            print(e)
            print("Too much conversation! Dumping history.")
            print(state)
            state = [("system", "You are a helpful assistant")]
            
            # Yield an error response
            yield [("system", "An error occurred. History has been reset.")]

# Instantiate Conversation and Gradio interface
conversation = Conversation()
demo = gr.Interface(
    fn=conversation.predict,
    inputs=gr.Textbox(lines=2, placeholder="Enter your message here..."),
    outputs=gr.Chatbot(),
    examples=[["hello"], ["hola"], ["error"]],
    title="Conversation Interface"
)
demo.launch()

# Launch the interface
iface.launch()
