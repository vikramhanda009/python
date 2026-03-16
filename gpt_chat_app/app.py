import os
import traceback
from pathlib import Path

from flask import Flask, render_template, request, jsonify
from openai import OpenAI

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

GROQ_KEY = os.environ.get("OPENAI_API_KEY")

GROQ_BASE = os.environ.get(
    "OPENAI_BASE_URL",
    "https://api.groq.com/openai/v1"
)

GROQ_MODEL = os.environ.get(
    "OPENAI_MODEL",
    "llama-3.3-70b-versatile"
)

IMAGE_KEY = os.environ.get("IMAGE_API_KEY")

print("CHAT MODEL:",GROQ_MODEL)
print("GROQ KEY:",bool(GROQ_KEY))
print("IMAGE KEY:",bool(IMAGE_KEY))


# ========================
# CHAT AI
# ========================

def ask_ai(user_input):

    if not GROQ_KEY:
        raise ValueError("Groq API key missing")

    client = OpenAI(

        api_key=GROQ_KEY,

        base_url=GROQ_BASE

    )

    response = client.chat.completions.create(

        model=GROQ_MODEL,

        messages=[

            {
                "role":"system",
                "content":"You are a helpful assistant."
            },

            {
                "role":"user",
                "content":user_input
            }

        ],

        temperature=0.7,

        max_tokens=500

    )

    return response.choices[0].message.content


# ========================
# IMAGE AI
# ========================

def image(prompt):

    if not IMAGE_KEY:
        raise ValueError("Image API key missing")

    image_client = OpenAI(

        api_key=IMAGE_KEY

    )

    result = image_client.images.generate(

        model="gpt-image-1",

        prompt=prompt,

        size="1024x1024"

    )

    return result.data[0].url


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

        user_input=data.get("message","")

        if not user_input.strip():

            return jsonify({

                "error":"Message required"

            }),400

        reply=ask_ai(user_input)

        return jsonify({

            "reply":reply

        })

    except Exception:

        print(traceback.format_exc())

        return jsonify({

            "error":"Chat failed"

        }),500


@app.route('/image',methods=['POST'])
def image():

    try:

        data=request.get_json(silent=True) or {}

        prompt=data.get("prompt","")

        if not prompt.strip():

            return jsonify({

                "error":"Prompt required"

            }),400

        image_url=generate_image(prompt)

        return jsonify({

            "image":image_url

        })

    except Exception:

        print(traceback.format_exc())

        return jsonify({

            "error":"Image generation failed"

        }),500


# ========================
# START
# ========================

if __name__=="__main__":

    app.run(

        host="0.0.0.0",

        port=5001,

        debug=True

    )