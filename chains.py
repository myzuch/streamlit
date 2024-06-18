from langchain_openai import ChatOpenAI
from prompts import *


def get_summary(input_text, sections, model="gpt-3.5-turbo", by_sections=False):
    if by_sections:
        summary = ""
        for section in sections:
            summary += get_summary_section(input_text, section) + "\n"
    else:
        num_sections = len(sections)
        sections = str(sections).strip("[]")
        system_prompt = SYSTEM_PROMPT.format(
            sections=sections, num_sections=num_sections
        )
        user_prompt = f"Summarise the following note: \n{input_text}"
        messages = prompts_to_messages(system_prompt, user_prompt)
        llm = ChatOpenAI(temperature=0, model=model)
        summary = llm.invoke(messages).content
    return summary


def get_summary_section(input_text: str, section: str, model="gpt-3.5-turbo"):
    section_description = SECTIONS[section]
    system_prompt = SECTION_PROMPT.format(
        section=section, description=section_description
    )
    user_prompt = f"Summarise the following note: \n{input_text}"
    messages = prompts_to_messages(system_prompt, user_prompt)
    prompt = apply_chat_template(messages, model)
    llm = ChatOpenAI(temperature=0, model=model)
    summary_section = llm.invoke(prompt).content
    return summary_section


def prompts_to_messages(system_prompt, user_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    return messages


def apply_chat_template(messages, model_type="none"):
    template_tokens = MODEL_TEMPLATE_TOKENS.get(
        model_type,
        {
            "begin_token": "",
            "system_start": "",
            "user_start": "",
            "assistant_start": "",
            "end_token": "",
        },
    )
    prompt = template_tokens["begin_token"]

    for message in messages:
        role = message["role"]
        start_token = template_tokens[f"{role}_start"]
        content = message["content"]
        end_token = template_tokens["end_token"]
        prompt += f"{start_token}\n{content}{end_token}\n"

    prompt += template_tokens["assistant_start"] + "\n"
    return prompt
