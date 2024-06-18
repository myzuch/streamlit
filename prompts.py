MODEL_TEMPLATE_TOKENS = {
    'llama-3': {
        'begin_token': '<|begin_of_text|>',
        'system_start': '<|start_header_id|>system<|end_header_id|>',
        'user_start': '<|start_header_id|>user<|end_header_id|>',
        'assistant_start': '<|start_header_id|>assistant<|end_header_id|>',
        'end_token': '<|eot_id|>',
    },
    'gpt-3.5-turbo':{'begin_token': '',
        'system_start': '',
        'user_start': '',
        'assistant_start': '',
        'end_token': '',}
}

SECTIONS = {
    "Social History": """Provide a summary of the patient's social history, including relevant details such as:

    Tobacco, alcohol, or substance use
    Living situation and social support network
    Occupational history and any relevant job-related exposures or hazards
    Cultural or spiritual beliefs that may impact their healthcare
""",
    "Allergies": """
    List any allergies the patient has, including reactions and their severity. Detail any relevant information such as triggers, symptoms, and any necessary precautions or treatments. If the patient has no known allergies, please state "No relevant information."
    """,
    "Medications": """
    Please provide a list of the patient's current medications, including:

    Medication names
    Dosage and frequency
    Start and end dates (if applicable)
    Any relevant instructions or precautions
    If the patient is not taking any medications, please state "No medications at this time." Use markdown formatting for your response.""",
    "Problems": "",
    "Author of transaction": "",
}

SYSTEM_PROMPT = """
You are a medical summarization assistant. Your task is to read thoroughly through a patient's medical note and provide a concise extractive summary in a clear and engaging manner covering the key information.

The summary should have {num_sections} main sections: {sections}. Include any relevant information from the note into a corresponding section. Each section should be comprehensive and represent the most relevant information about the patient health. Information in each section should be represented as a list.

Please begin each section with the corresponding header.
Focus on extracting just the core medical details needed. Avoid introductory phrases.
For those sections where no relevant information is found, simply state "No relevant information."
Use markdown formatting.
"""

SECTION_PROMPT = """
You are a medical summarization assistant. Your task is to read thoroughly through a patient's medical note and provide a concise extractive summary of {section} in a clear and engaging manner covering the key information.
{description}
Include any relevant information from the note into a corresponding section. The section should be comprehensive and represent the most relevant information about the patient health. Information in the section should be represented as a list.

Please begin section with the corresponding header.
Focus on extracting just the core medical details needed. Avoid introductory phrases.
If there is no relevant information is for the section, simply state "No relevant information."
Please provide a concise list, using markdown formatting.
"""
