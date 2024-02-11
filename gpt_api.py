import os
import json
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()  

app = Flask(__name__)
client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY"),
)

@app.route('/api/description', methods=['GET'])
def get_descript():
    completion = client.chat.completions.create(
        model="gpt-4",
        max_tokens=800,
        messages=[
            {"role": "assistant", "content": f"Describe a term from a financial point of view, options trading. the user is possibly a college student, learning about a new concept \
                or in a perplexity about the term in the context. I will need you to give a short and concise description"}
        ]
    )
    print(jsonify(completion.choices[0].message.content))
    return jsonify(completion.choices[0].message.content)
    

@app.route('/api/example', methods=['GET'])
def get_example():
    completion = client.chat.completions.create(
        model="gpt-4",
        max_tokens=200,
        messages=[
            {"role": "assistant", "content": f"provide a descriptive example to illustrate the financial/economic concept with a real-life example to demonstrate clear understanding"}
        ]
    )
    print(completion.choices[0].message.content)
    return jsonify(completion.choices[0].message.content)


if __name__ == '__main__':
    app.run(debug=True)


