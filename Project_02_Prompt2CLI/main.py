import gradio as gr
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

clientq = OpenAI(
    base_url=os.getenv("URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)
def safety_filter(command):
    """
    פונקציה שבודקת אם הפקודה מכילה ביטויים אסורים לפי דרישות המטלה.
    """
    forbidden_terms = ["rm -rf", "del", "shutdown", "format", "system32", "mkfs", "/etc", "/bin"]
    cmd_lower = command.lower()
    for term in forbidden_terms:
        if term in cmd_lower:
            return "ERROR: Unauthorized Destructive Command"
    return command

def text_to_terminal_agent(user_prompt):
    logic_prompt = f"""
    You are a professional Technical Assistant specialized in translating natural language prompts into terminal/CLI commands.
    STRICT OUTPUT RULES:
    Output ONLY the raw, executable command string.
    NO explanations, NO introductory text, NO conversational filler, and NO markdown formatting (no backticks).
    SAFETY: If a user request involves destructive actions (e.g., deleting system directories like /system32, /etc, /bin, formatting drives, or shutting down the system), you must output exactly one word: ERROR. Do not provide the command and do not provide a warning message.
    BEHAVIOR EXAMPLES:
    If the user says "List files in the current directory", reply: ls (or dir on Windows).
    If the user says "Show me the current date and time", reply: date.
    If the user says "Create a new directory called 'test'", reply: mkdir test.
    If the user says "Remove a file named 'example.txt'", reply: rm example.txt.
    If the user says "Move a file named 'example.txt' to a directory called 'backup'", reply: mv example.txt backup/.
    If the user says "Copy a file named 'example.txt' to a directory called 'backup'", reply: cp example.txt backup/.
    If the user says "Display the contents of a file named 'example.txt'", reply: cat example.txt.
    If the user says "Find all files containing the word 'report' in their name", reply: ls *report*.
    If the user says "Show me the disk usage of the current directory", reply: du -h.
    If the user says "Check if a process named 'python' is running", reply: pgrep python.
    TECHNICAL STANDARDS:
    ACCURACY: If the request includes counting or summing, the command must execute both.
    EFFICIENCY: Prefer 'awk' for text processing and calculations. Avoid unnecessary pipes.
    ROBUSTNESS: Ensure commands handle edge cases like empty files or missing directories.
    NETWORK: Use 'curl -IsL' for website checks to follow redirects efficiently.
    VALIDITY: Use only valid flags for standard GNU/BSD/Windows tools.
    REMEMBER: If the command is dangerous, output "ERROR" only. If it is safe, output the command and NOTHING else.
    """

    responseq = clientq.chat.completions.create(
        model=os.getenv("MODEL_NAME"), 
        messages=[
            {"role": "system", "content": logic_prompt}, 
            {"role": "user", "content": user_prompt}
        ],
        temperature=0
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