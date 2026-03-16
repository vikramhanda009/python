import os
import traceback
from pathlib import Path

from flask import Flask, render_template, request, jsonify
from langchain_groq import ChatGroq
from prompts import build_story_prompt, get_user_input

app = Flask(__name__)

# ========================
# LOAD ENV
# ========================

env_path = Path(__file__).resolve().parent / ".env"

if env_path.exists():

    for line in env_path.read_text().splitlines():

        line=line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key,val=line.split("=",1)

        os.environ[key.strip()] = val.strip().strip('"').strip("'")

# ========================
# CONFIG
# ========================

GROQ_KEY=os.environ.get("OPENAI_API_KEY")

GROQ_MODEL=os.environ.get(

    "OPENAI_MODEL",

    "llama-3.3-70b-versatile"

)

print("MODEL:",GROQ_MODEL)

print("KEY FOUND:",bool(GROQ_KEY))


# ========================
# LANGCHAIN AI
# ========================

llm = ChatGroq(

    api_key=GROQ_KEY,

    model=GROQ_MODEL,

    temperature=0.7

)


def ask_ai(character,setting,genre,theme):

    prompt = build_story_prompt(

        character,

        setting,

        genre,

        theme

    )

    response = llm.invoke(prompt)

    return response.content


# ========================
# ROUTES
# ========================

@app.route('/')
def index():

    return render_template("index.html")


@app.route('/response',methods=['POST'])
def response():

    try:

        data=request.get_json(silent=True) or {}

        character=data.get("character","hero")

        setting=data.get("setting","future city")

        genre=data.get("genre","sci-fi")

        theme=data.get("theme","hope")

        reply=ask_ai(

            character,

            setting,

            genre,

            theme

        )

        return jsonify({

            "reply":reply

        })

    except Exception:

        print(traceback.format_exc())

        return jsonify({

            "error":"Story generation failed"

        }),500


# ========================
# START
# ========================
if __name__=="__main__":

    mode = input("Run mode (cli/server): ").strip()

    if mode=="cli":
        c,s,g,t = get_user_input()
        print(ask_ai(c,s,g,t))

    else:

        app.run(

            host="0.0.0.0",

            port=5002,

            debug=True

        )