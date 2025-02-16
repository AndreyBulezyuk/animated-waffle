## Setup Helpers in .vscode for automatic formatting with black on save
see settings.json

## Arguments
1. I have no experience with htmx, that is why i'll to stick to the
principles of separation of concerns and keep the backend and frontend as separated as possible. Meaning, no HTML/HTMX in the backend code.



# Prompts used with ChatGPT o3-mini-high:
```
Role: You are an advanced AI that supports me in creating highly scalable, secure, fail-tolerant code and applications. 
Requirements:
1. All code must be fail-tolerant, meaning every fail possibility must be catched.
2. All code must be written in best practices for the python3.13 and django 5.
3. Code must have comments in section that have complex code section. Comments must also be present in areas where business logic behind the code should be explained.
4. Use most current versions, packages, frameworks, plugins, structures, and similar components.

Constraints:
1. Don't talk too much, the reader of you text and code is highly experienced. Provide more copy-paste code and bash commands. 


Give me a bootstrap template for django 5 + htmx + bootstrap. Application pages should be able to CRUD data without full page reload.
```


```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
pip3 install -r requirements-dev.txt
```