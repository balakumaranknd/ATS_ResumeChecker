def extract_experience_lines(resume_text):
    lines = resume_text.split("\n")

    bullets = []

    for line in lines:
        line = line.strip()

        # Only pick lines that look like real bullets
        if (
            len(line) > 50 and
            (
                line.startswith("-") or
                line.startswith("•") or
                line.startswith("*") or
                line[0].isdigit()
            )
        ):
            bullets.append(line)

    return bullets[:5]