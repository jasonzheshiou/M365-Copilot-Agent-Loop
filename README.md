# M365-Copilot-Agent-Loop 🚀

Turn your standard Microsoft 365 Copilot chatbox into an autonomous, self-correcting agentic coding loop—similar to OpenCode, Claude Engineer, or Devin. 

This framework acts as a bridge. It leverages your native **OneDrive cloud sync** to pass code modifications directly to your local computer, executes them, logs terminal output or errors, and prepares feedback logs to drop back into Copilot.

---

## ⚠️ Context & Project Status (Please Read First)
Author Background: I am an Actuary working within the AI Working Group. 

Project Status: UNTESTED CONCEPTUAL BLUEPRINT. 
Many actuaries and enterprise professionals operate in locked-down corporate environments where they only have access to the standard M365 Copilot web/Teams interface. Dedicated agentic coding frameworks cannot be installed. This repository was created as an open idea-sharing playground to solve that limitation. 

Development Context: I collaborated with Google AI to derive and structure this technical workflow framework. The code provided here has not been thoroughly live-tested yet, but I plan to test it extensively. 

📢 Call for Collaboration: I am opening this up to the community immediately to invite fellow actuaries, developers, and data professionals to try this methodology, break it, patch it, and share ideas via GitHub Issues and Pull Requests!



## How It Works (The Core Loop)
1. **Plan & Write:** You prompt M365 Copilot to write or update a `.py` script based on instructions.
2. **Sync:** Copilot outputs the code block, and you save it directly over the target file in your local `Microsoft Copilot Chat Files` OneDrive folder.
3. **Execute:** This local watcher script detects the updated file, executes it in an isolated local terminal, and catches stdout/stderr.
4. **Log:** The script outputs a local file called `execution_log.txt`.
5. **Feed:** You upload `execution_log.txt` back to the chatbox to close the loop, allowing Copilot to self-correct if it failed or move to the next step if it passed.

---

## Project Structure

```text
├── README.md               # This documentation file
├── copilot_agent.py        # The local file-system watcher and executor script
└── AGENTIC_RULES.md       # The system prompt context file you upload to Copilot
```

---

## 🛠️ Setup Instructions

### 1. Prerequisites
Install the required system file-watcher library in your local terminal environment:
```bash
pip install watchdog
```

### 2. Configure the Watcher (`copilot_agent.py`)
Save the code below as `copilot_agent.py`. Make sure to update the `WATCH_FOLDER` path string to point to your specific local OneDrive folder location.

```python
import os
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# UPDATE THIS TO MATCH YOUR LOCAL ONEDRIVE DIRECTORY LOCATION
WATCH_FOLDER = os.path.expanduser("~/OneDrive/Microsoft Copilot Chat Files")
LOG_FILE = os.path.join(WATCH_FOLDER, "execution_log.txt")

class CopilotAgentHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".py") and "copilot_agent.py" not in event.src_path:
            self.process_file(event.src_path)

    def process_file(self, file_path):
        print(f"\n🤖 Agent Loop Triggered: Copilot updated {os.path.basename(file_path)}")
        print("⚡ Executing script and logging outputs...")
        
        # Debounce time window for filesystem write operations
        time.sleep(0.5)
        
        try:
            result = subprocess.run(
                ["python", file_path], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            output_content = f"--- COPIOT AGENT EXECUTION LOG ---\n"
            output_content += f"Target File: {os.path.basename(file_path)}\n"
            output_content += f"Status: {'SUCCESS' if result.returncode == 0 else 'FAILED'}\n\n"
            output_content += "STDOUT (Output):\n" + (result.stdout if result.stdout else "None\n")
            output_content += "\nSTDERR (Errors):\n" + (result.stderr if result.stderr else "None\n")
            
        except subprocess.TimeoutExpired:
            output_content = "Execution timed out after 30 seconds."
        except Exception as e:
            output_content = f"Local framework execution error: {str(e)}"

        with open(LOG_FILE, "w") as log:
            log.write(output_content)
        print("📝 execution_log.txt updated. Feed this back into M365 Copilot chat.")

if __name__ == "__main__":
    if not os.path.exists(WATCH_FOLDER):
        print(f"Error: Path '{WATCH_FOLDER}' does not exist. Please check your config path variables.")
        exit(1)
        
    event_handler = CopilotAgentHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()
    print(f"🚀 OpenCode-style local agent active. Watching: {WATCH_FOLDER}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

### 3. Create the Rules Document (`AGENTIC_RULES.md`)
Save the text below as `AGENTIC_RULES.md`. Upload this file along with your target code files to M365 Copilot at the beginning of every single session.

```markdown
# Agent Identity & System Prompt
You are an autonomous Agentic Software Engineer operating inside an M365 environment. You must strictly adhere to the OpenCode framework rules outlined below.

## Execution Constraints
1. **Never write code blindly**: Review the state of the existing code before changing functions.
2. **File Generation Rules**: When you produce code modifications, format the code cleanly and instruct the user: "Save this exact block to your local environment file."
3. **Handle Errors Iteratively**: If the user provides an execution log showing a failure, your priority is to find the root cause, document it in an internal scratchpad, and provide an adjusted code script targeting that error.

## Step-by-Step Task Loop
- **Step 1 (Ingest & Analyze)**: Read the uploaded code and `AGENTIC_RULES.md`. Acknowledge that the agent profile is active.
- **Step 2 (Plan)**: Outline a 3-step sequence of structural code alterations. Wait for user approval.
- **Step 3 (Deliver File)**: Output the target code block clearly.
- **Step 4 (Read Log)**: Evaluate the incoming `execution_log.txt` generated by the local python watcher script. Adjust execution path dynamically based on output.
```

---

## ⚠️ Important License & Corporate Security Warning

Before running or deploying this code in a corporate enterprise workspace, review these critical security boundaries:

1. **Human-In-The-Loop Security:** This architecture requires a manual copy-paste step by design. This acts as an air-gap security feature. Never use automated macro injection utilities to auto-send prompts to your M365 environment, as this violates corporate browser safety policies and standard terms of service.
2. **Intellectual Property Shield:** When uploading rules or text to public GitHub repositories, ensure you strip out all enterprise code samples, internal database endpoints, private secrets, API authorization keys, or corporate schemas. Keep your rules purely generic.

---

## 📄 License

### MIT License

Copyright (c) 2026 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS-IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
