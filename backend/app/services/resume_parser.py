import fitz
from docx import Document



def extract_text(filepath: str, file_type: str):

    text = ""


    if file_type == "application/pdf":

        pdf = fitz.open(filepath)

        for page in pdf:
            text += page.get_text()


    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":

        doc = Document(filepath)

        for para in doc.paragraphs:
            text += para.text + "\n"


    return text



def extract_skills(text: str):

    skills_list = [
        "Python",
        "Java",
        "C++",
        "React",
        "FastAPI",
        "Django",
        "Machine Learning",
        "Deep Learning",
        "SQL",
        "PostgreSQL",
        "TensorFlow",
        "PyTorch",
        "JavaScript",
        "TypeScript",
    ]


    found = []


    lower_text = text.lower()


    for skill in skills_list:

        if skill.lower() in lower_text:
            found.append(skill)


    return ", ".join(found)



def extract_languages(text:str):

    languages = [
        "English",
        "Nepali",
        "Hindi",
    ]

    found=[]

    lower=text.lower()

    for lang in languages:

        if lang.lower() in lower:
            found.append(lang)


    return ", ".join(found)



def extract_projects(text:str):

    lines=text.split("\n")

    projects=[]

    for line in lines:

        if "project" in line.lower():

            projects.append(line.strip())


    return ", ".join(projects)



def extract_experience(text:str):

    lines=text.split("\n")

    experience=[]

    for line in lines:

        if (
            "experience" in line.lower()
            or "intern" in line.lower()
            or "developer" in line.lower()
        ):
            experience.append(line.strip())


    return ", ".join(experience)