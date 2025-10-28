# generator.py
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# 🔹 Choose a lightweight model (runs on CPU)
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Load model once globally (slow first time)
print(f"⏳ Loading model: {MODEL_NAME} ...")
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="auto", torch_dtype="auto")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
print("✅ Model loaded successfully!")

def build_prompt(context_chunks, query):
    ctx = "\n\n".join([c["text"] for c in context_chunks])
    prompt = (
        "You are a helpful assistant. Answer only using the provided context below.\n\n"
        f"Context:\n{ctx}\n\n"
        f"Question: {query}\n\nAnswer:"
    )
    return prompt

def generate_answer(context_chunks, query, max_new_tokens=150):
    try:
        prompt = build_prompt(context_chunks, query)

        response = generator(
            prompt,
            max_new_tokens=max_new_tokens,
            temperature=0.3,
            do_sample=True,
            top_p=0.9,
        )

        text = response[0]["generated_text"]
        # Extract answer after "Answer:"
        answer = text.split("Answer:")[-1].strip()
        return answer or "No response generated."
    except Exception as e:
        return f"(Error during generation: {e})"
