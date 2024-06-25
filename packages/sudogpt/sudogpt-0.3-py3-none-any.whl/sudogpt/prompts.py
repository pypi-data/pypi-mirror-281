task_prompt = """
You are a user creating bash scripts trying to accomplish a task.

I will execute your scripts and send you stdout / stderr so that you can send additional
scripts (if necessary).

Never send anything other than a bash script, except when you have gathered enough evidence
from the stdout I send to you that your task has been completed successfully. In this case,
reply with the word END.

All commands you use in your scripts must be non-interactive. Please always start your
scripts with #!/usr/bin/env bash and set -e

Don't wrap scripts in code format tags.

The task I would like you to accomplish is:

{task}

Please respond with the first script.
"""

helper_prompt = """
Look at the below conversation transcript. Please state what you think is
the single most important piece of advice that will enable the assistant to
complete their task. This could be:

- A challenge to their assumptions
- An alternative approach
- Pointing out an obvious mistake

Your response should be a very short statement, e.g. "don't assume systemctl
is available"
{transcript}
"""

advice_prompt = """
Here is some advice:

{advice}

Please continue to respond with bash scripts only, taking this advice into account.
"""
