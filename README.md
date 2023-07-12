# Power tools for more efficient use of Microsoft ToDo for GTD

Some functionality that's missing in ToDo (in my opinion) for making it a great tool for GTD.

- Finding stale acitons
- Are there projects that don't have a next aciton/waiting item?
- Measuring flow

# Requirements

Get a auth token e.g. in https://developer.microsoft.com/en-us/graph/graph-explorer. Full-blown authorization is not supported at the moment.

# Running

- Get the token, put it into your `config.json` (use the template to get started).
- `python powerGToDo.py`

For development purposes, the script will spit out a pickle file so that the todos won't be fetched from the MS Grid API on every run.

[![Unit tests](https://github.com/dhesse/powerGToDo/actions/workflows/test.yml/badge.svg)](https://github.com/dhesse/powerGToDo/actions/workflows/test.yml)
