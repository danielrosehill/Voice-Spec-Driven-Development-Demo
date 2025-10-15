This repository contains a model for a multi-agent framework intended to take an audio recording of a software specification and then begin the project.

The framework is intended to run locally (first as a POC CLI then maybe a lightweight GUI).

The agents are:

1 - Transcribe and optimise development prompt (Gemini)
2 - Start the repo with GH CLI (could be substituted for GH MCP but for the moment I prefer the CLI). Create a CLAUDE.md in the repo.
3 - Start off the project with a first sprint (Claude CLI suggested)

Note: I'm not envisioning that this will use local AI. Although its run on the local, the integrations will be with cloud LLMs via APIs

Between steps 2 and 3 we have a change of CWD as the agent now needs to work in the newly created repo 

Ideally the system would flow from 1 to 3 with a success message showing to the user after 3 along the lines of "the project has been kicked off here, {link to local path and repo online}

There is now an abundance of multi agent AI framworks out there and my philosophy is that it's always better to build on existing components than try to reinvent wheels.

Can you suggest several that would be particularly suitable for this agentic workflow? After providing your suggestions, I will make a selection'

The language is not set in stone/ dont constrain your recommendations based on JS/Python

Please use search to make sure that you are drawing upon up to date information

