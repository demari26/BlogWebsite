from openai import OpenAI
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

ai = Blueprint("ai_routes", __name__)


@ai.route("/api/ai/generate/blog")
def generate_blog():
    title = request.args.get("title")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        # response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "500 words output"},
            {"role": "user", "content": f"Generate a blog about {title}"}
        ]
    )
    return jsonify(title=title, message=completion.choices[0].message.content)