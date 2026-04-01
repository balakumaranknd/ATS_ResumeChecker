import re

def normalize_text(text):
    # join broken characters
    text = re.sub(r'(\w)\n(\w)', r'\1\2', text)

    # normalize newlines
    text = re.sub(r'\n+', '\n', text)

    # remove excessive spaces
    text = re.sub(r'[ \t]+', ' ', text)

    return text.strip()


def fix_section_headers(text):
    sections = [
        "PROFESSIONAL SUMMARY",
        "EXPERIENCE",
        "PROJECTS",
        "SKILLS",
        "EDUCATION",
        "CERTIFICATIONS"
    ]

    for sec in sections:
        # Add newline BEFORE section if missing
        text = re.sub(rf"(?<!\n)({sec})", r"\n\1", text)

        # Add newline AFTER section if missing
        text = re.sub(rf"({sec})(?!\n)", r"\1\n", text)

    return text

def extract_sections(text):
    section_titles = [
        "PROFESSIONAL SUMMARY",
        "EXPERIENCE",
        "PROJECTS",
        "SKILLS",
        "EDUCATION",
        "CERTIFICATIONS"
    ]

    sections = {}
    current_section = "header"
    sections[current_section] = ""

    for line in text.split("\n"):
        line = line.strip()

        if line.upper() in section_titles:
            current_section = line.lower()
            sections[current_section] = ""
        else:
            sections[current_section] += line + " "

    return sections

def parse_experience(exp_text):
    entries = []
    lines = exp_text.split("\n")

    current = {}

    for line in lines:
        line = line.strip()

        # detect company + role
        if "–" in line or "-" in line:
            if current:
                entries.append(current)
                current = {}

            current["meta"] = line
            current["description"] = ""

        else:
            current.setdefault("description", "")
            current["description"] += line + " "

    if current:
        entries.append(current)

    return entries

def build_structured_resume(raw_text):
    text = normalize_text(raw_text)
    text = fix_section_headers(text)   # 🔥 ADD THIS
    sections = extract_sections(text)

    return {
        "header": sections.get("header", ""),
        "summary": sections.get("professional summary", ""),
        "experience": parse_experience(sections.get("experience", "")),
        "projects": sections.get("projects", ""),
        "skills": sections.get("skills", ""),
        "education": sections.get("education", ""),
        "certifications": sections.get("certifications", "")
    }