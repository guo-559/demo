import gradio as gr
from openai import OpenAI

# Initialize the OpenAI client with the server details
client = OpenAI(base_url="http://10.254.50.50:8001/v1", api_key="not-used")
conversation_history = [{"role": "system", "content": " You are a helpful assistant"}]
print(conversation_history)

def predict(prompt, history):
    """
    Get response from OpenAI API based on prompt.
    """

    # TODO: do u need this globals, fix this shit
    
    if 'conversation_history' not in globals():
        # If conversation_history doesn't exist, create it
        global conversation_history
        conversation_history = [{"role": "user", "content": prompt}]     
    else:
        # Append the new prompt to the conversation history as a user message
        conversation_history.append({"role": "user", "content": prompt})


    try:
        # different from client.completions endpoint
        response = client.chat.completions.create(
            model="meta/llama3-70b-instruct",
            max_tokens=2000,
            stream=True,
            temperature=0.2,
            messages=conversation_history, # needed for chat TODO: system message etc.
            top_p=0.3
        )

        partial_msg = ""

        # Combine chunks into a full response (since gradio cannot stream)
        for chunk in response:
            if hasattr(chunk, 'choices') and len(chunk.choices) > 0 and chunk.choices[0].delta.content:
                partial_msg = partial_msg + chunk.choices[0].delta.content
                yield partial_msg

        conversation_history.append({"role": "assistant", "content": partial_msg})
    except Exception as inst:
        print(inst)
        print("Too much conversation! dumping history")
        print(conversation_history)
        conversation_history = []
 

# Create a Gradio ChatInterface
demo = gr.ChatInterface(
    fn=predict,
    examples=[{"text": "hello"}, {"text": "hola"}, {"text": "merhaba"}],
    title="PTC System (S) Pte Ltd llama3-70b",
    multimodal=False
)
demo.launch(share=True)

