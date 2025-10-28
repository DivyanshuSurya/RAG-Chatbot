from flask import Flask, request, jsonify, render_template
from retriever import Retriever
from generator import generate_answer
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
retriever = Retriever()  # initialize retriever once

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        query = data.get("query", "")
        if not query:
            return jsonify({"answer": "Please enter a query."})

        # Retrieve top chunks
        context_chunks = retriever.retrieve(query, top_k=4)
        if not context_chunks:
            return jsonify({"answer": "No relevant context found."})

        # Generate final answer
        answer = generate_answer(context_chunks, query)
        return jsonify({"answer": answer})

    except Exception as e:
        print("⚠️ Error in /chat:", e)
        return jsonify({"answer": f"Error: {e}"})

if __name__ == "__main__":
    app.run(port=5600, debug=True)
