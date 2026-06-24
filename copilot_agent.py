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
