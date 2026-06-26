from flask import Flask, render_template, request
import joblib
import pdfplumber
import re
import nltk

from nltk.corpus import stopwords


# -----------------------------
# NLTK
# -----------------------------

nltk.download("stopwords")


# -----------------------------
# Flask setup
# -----------------------------

app = Flask(__name__)


# -----------------------------
# Load ML files
# -----------------------------

model = joblib.load(
    "models/resume_model.pkl"
)

vectorizer = joblib.load(
    "models/tfidf_vectorizer.pkl"
)


stop_words = set(
    stopwords.words("english")
)



# -----------------------------
# Extract PDF text
# -----------------------------

def extract_text(file):

    text = ""

    try:

        with pdfplumber.open(file) as pdf:

            for page in pdf.pages:

                data = page.extract_text()

                if data:

                    text += data


    except Exception as e:

        print("PDF ERROR:", e)


    return text





# -----------------------------
# Clean text
# -----------------------------

def clean_text(text):

    text = text.lower()


    text = re.sub(
        "[^a-zA-Z]",
        " ",
        text
    )


    words = text.split()


    words = [

        w for w in words

        if w not in stop_words

    ]


    return " ".join(words)





# -----------------------------
# Find skills
# -----------------------------

def get_skills(text):

    skills = [

        "python",
        "java",
        "sql",
        "html",
        "css",
        "javascript",
        "react",
        "flask",
        "django",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "git",
        "github",
        "excel",
        "aws"

    ]


    found = []


    text = text.lower()


    for skill in skills:

        if skill in text:

            found.append(skill)


    return found





# -----------------------------
# Resume score
# -----------------------------

def resume_score(text, skills):

    score = 0


    keywords = [

        "education",
        "project",
        "experience",
        "skills"

    ]


    for k in keywords:

        if k in text.lower():

            score += 15



    score += len(skills) * 5


    return min(score,100)





# -----------------------------
# Home page
# -----------------------------

@app.route("/")

def home():

    return render_template(
        "index.html"
    )






# -----------------------------
# Analyze
# -----------------------------

@app.route(
    "/predict",
    methods=["POST"]
)

def predict():


    print("ANALYSIS STARTED")



    file = request.files.get("resume")


    if not file:

        return "No file selected"




    print("FILE:", file.filename)




    text = extract_text(file)



    print("TEXT LENGTH:", len(text))


    print(text[:300])



    if len(text)==0:

        return "PDF text not readable"





    cleaned = clean_text(text)



    data = vectorizer.transform(
        [cleaned]
    )



    prediction = model.predict(
        data
    )



    role = prediction[0]



    skills = get_skills(text)



    score = resume_score(
        text,
        skills
    )



    print("----------------")

    print("ROLE:", role)

    print("SKILLS:", skills)

    print("SCORE:", score)

    print("----------------")




    return render_template(

        "result.html",

        role=role,

        skills=skills,

        score=score

    )







# -----------------------------
# Run Flask
# -----------------------------

if __name__ == "__main__":

    print("FLASK SERVER STARTING")

    app.run(
        debug=True
    )