import gradio as gr
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

clientq = OpenAI(
    base_url=os.getenv("URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

def text_to_terminal_agent(user_prompt):
    logic_prompt = f"""
    You are a helpful assistant that translates user prompts into terminal commands.
    If the user says "List files in the current directory", you should reply with "ls".
    If the user says "Show me the current date and time", you should reply with "date".
    If the user says "Create a new directory called 'test'", you should reply with "mkdir test".
    If the user says "Remove a file named 'example.txt'", you should reply with "rm example.txt".
    If the user says "Move a file named 'example.txt' to a directory called 'backup'", you should reply with "mv example.txt backup/".
    If the user says "Copy a file named 'example.txt' to a directory called 'backup'", you should reply with "cp example.txt backup/".
    If the user says "Display the contents of a file named 'example.txt'", you should reply with "cat example.txt".
    If the user says "Find all files containing the word 'report' in their name", you should reply with "ls *report*".
    If the user says "Show me the disk usage of the current directory", you should reply with "du -h".
    If the user says "Check if a process named 'python' is running", you should reply with "pgrep python".
    Output ONLY the raw command text. 
    No explanations, no conversational filler, no markdown blocks.
    """

    responseq = clientq.chat.completions.create(
        model=os.getenv("MODEL_NAME"), 
        messages=[
            {"role": "system", "content": logic_prompt}, 
            {"role": "user", "content": user_prompt}
        ],
    )
    temperature=0
    commandq = responseq.choices[0].message.content.strip()
    clean_command = commandq.replace("`", "").strip()
    return clean_command
    
with gr.Blocks(title="AI Terminal Agent") as demo:
    gr.Markdown("### 🤖 Groq Terminal Agent")
    
    with gr.Column():
        input_text = gr.Textbox(
            label="הוראה בשפה חופשית", 
            placeholder="למשל: Show me the current date"
        )
        output_command = gr.Code(
            label="הפקודה להעתקה", 
            interactive=False,
            show_label=True
        )
    run_btn = gr.Button("חלץ פקודה")
    input_text.submit(fn=text_to_terminal_agent, inputs=input_text, outputs=output_command)
    run_btn.click(fn=text_to_terminal_agent, inputs=input_text, outputs=output_command)
        

if __name__ == "__main__":
    demo.launch()