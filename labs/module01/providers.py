"""Run: python module01/providers.py openai OR huggingface."""
import os
import sys

PROMPT = "Explain a Python dictionary in two sentences for a beginner."

def main(provider):
    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(timeout=45, max_retries=2)
        response = client.responses.create(
            model=os.environ["OPENAI_MODEL"],
            instructions="You teach introductory Python clearly.",
            input=PROMPT,
            max_output_tokens=500,
        )
        print(response.output_text)
        print("Usage:", response.usage)
    elif provider == "huggingface":
        from huggingface_hub import InferenceClient
        client = InferenceClient(provider="auto", api_key=os.environ["HF_TOKEN"], timeout=45)
        result = client.chat.completions.create(
            model=os.environ["HF_MODEL"],
            messages=[{"role": "user", "content": PROMPT}],
            max_tokens=200,
        )
        print(result.choices[0].message.content)
    else:
        raise SystemExit("Choose openai or huggingface")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "openai")
