import openai
from translate import Translator
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
openai.api_key = "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"

translator = Translator(to_lang="my")


@app.route("/")
def index():
    return render_template("index.html")


def translate_to_myanmar(text):
    try:
        translation = translator.translate(text)
        return translation
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return ""


@app.route("/chat", methods=["POST"])
def chat():
    ask = request.json["message"]

    if ask == "break":
        return jsonify({"response": "Thank you"})
    else:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=ask,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"],
        )
        returnPond = translate_to_myanmar(response["choices"][0]["text"])
        return jsonify({"response": returnPond})


if __name__ == "__main__":
    app.run(debug=True)
