import os
import stat
from datetime import datetime
from pathlib import Path
from subprocess import run

from openai import OpenAI

from .prompts import task_prompt, helper_prompt, advice_prompt


class OpenAIConversation(object):

    def __init__(self, openai_client=None, conversation=[]):

        self.client = openai_client or OpenAI()

        self.conversation = conversation

    def add_message(self, message, role="user"):

        msg = {"role": role, "content": message}
        self.conversation.append(msg)

    def next(self):
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=self.conversation,
        )
        msg = response.choices[0].message.content
        self.add_message(msg, role="assistant")
        return msg

    def as_text(self):
        text = "\n\n".join(
            [f"{m['role'].upper()}:\n\n{m['content']}" for m in self.conversation]
        )
        return text


class SudoGPT(object):

    def __init__(self, task, approve_scripts=True, use_helper=True):

        self.task = task
        
        self.approve_scripts = approve_scripts

        self.worker = SudoGPTWorker()

        self.helper = SudoGPTHelper(self.worker) if use_helper else None


    def get_approval(self, script):
        """
        Prompts the user to review and approve a script before executing it.

        Args:
            script (str): The script to be approved.

        Returns:
            None
        """
        print(f"script:\n\n{script}\n")
        answer = input("run this script? y/n: ")
        if answer != "y":
            exit()
        

    def go(self):
        # Prepare first message, specifying task
        msg = task_prompt.format(task=self.task)
        print(msg)

        # Enter task loop
        while True:
            script = self.worker.get_next_script(msg)

            if not script:
                return

            if self.approve_scripts:
                self.get_approval(script)

            self.worker.run_script()
            print(self.worker.script_result_str)

            if self.worker.script_counter % 2 == 0 and self.helper:
                help = self.helper.get_help()
                msg = advice_prompt.format(advice=help)
                print(msg)
            else:
                msg = None


class SudoGPTWorker(object):

    def __init__(self, conversation=None):

        # Conversation object for this task
        self.conversation = conversation or OpenAIConversation()

        # Latest response as string
        self.response = None

        # Latest script as string
        self.script = None

        # Number of executed scripts
        self.script_counter = 0

        # Path to latest script executable
        self.script_path = None

        # Latest script result (subprocess.CompletedProcess)
        self.script_result = None

        # Latest script result as formatted string
        self.script_result_str = None

        # State
        self.state = "init"

        # Generate a random working directory in which to save scripts
        self.working_dir = self.create_working_dir()

    def get_next_script(self, msg=None):
        if msg:
            self.conversation.add_message(msg)

        response = self.conversation.next()
        self.response = response

        if self.response_is_script(response):
            self.script = response
            self.script_path = self.save_script(response)
            return response

        else:
            self.state = "end"
            return None

    def response_is_script(self, response):
        return True if response.lower().startswith("#!") else False

    def save_script(self, script_str):
        script_path = os.path.join(self.working_dir, f"script_{self.script_counter}.sh")
        with open(script_path, "w") as f:
            f.write(script_str)

        # Make script executable
        st = os.stat(script_path)
        os.chmod(script_path, st.st_mode | stat.S_IEXEC)

        return script_path

    def run_script(self):
        result = run(f"./{self.script_path}", capture_output=True, shell=True, text=True)
        self.script_result = result
        self.script_result_str = self.script_result_to_str(self.script_result)
        self.save_script_result(self.script_result_str)
        self.conversation.add_message(self.script_result_str)
        self.script_counter += 1
        return result

    def save_script_result(self, script_result_str):

        result_path = os.path.join(
            self.working_dir, f"script_{self.script_counter}.sh.out"
        )

        with open(result_path, "w") as f:
            f.write(script_result_str)

    def script_result_to_str(self, script_result):

        # Truncate stdout / stderr to 1000 characters
        stdout = script_result.stdout[0:1000]
        stderr = script_result.stderr[0:1000]

        result_str = f"stdout:\n\n{stdout}\nstderr:\n\n{stderr}\n"
        return result_str

    def create_working_dir(self):
        job_id = datetime.now().strftime("%Y%m%d%H%M%S")
        working_dir = f".sudogpt/{job_id}"
        Path(working_dir).mkdir(parents=True)
        return working_dir


class SudoGPTHelper(object):

    def __init__(self, sudogpt, conversation=None):

        # Conversation object
        self.conversation = conversation or OpenAIConversation()

        self.worker = sudogpt

    def get_help(self):
        transcript = self.worker.conversation.as_text()
        self.conversation.add_message(helper_prompt.format(transcript=transcript))
        return self.conversation.next()













