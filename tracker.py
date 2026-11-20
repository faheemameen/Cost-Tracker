
import os
import sys
import time
import json

from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()


# ---------------- CONFIGURATION ----------------

GEMINI_MODEL = os.getenv("GEMINI_MODEL")
GROQ_MODEL = os.getenv("GROQ_MODEL")


GEMINI_INPUT_PRICE = 0.75
GEMINI_OUTPUT_PRICE = 3.75

GROQ_INPUT_PRICE = 0.075
GROQ_OUTPUT_PRICE = 0.30


# ---------------- GEMINI FUNCTION ----------------

def get_gemini_response(prompt):
    
    gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    start_time = time.perf_counter()

    response = gemini.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    elapsed_seconds = time.perf_counter() - start_time

    return {
        "provider": "Gemini",
        "model": response.model_version,
        "reply": response.text,
        "input_tokens": response.usage_metadata.prompt_token_count,
        "output_tokens": response.usage_metadata.candidates_token_count,
        "elapsed_seconds": elapsed_seconds
    }


# ---------------- GROQ FUNCTION ----------------

def get_groq_response(prompt):
    
    groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

    start_time = time.perf_counter()

    response = groq.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    elapsed_seconds = time.perf_counter() - start_time

    return {
        "provider": "Groq",
        "model": response.model,
        "reply": response.choices[0].message.content,
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens,
        "elapsed_seconds": elapsed_seconds
    }


# ---------------- CALCULATE COST ----------------

def calculate_cost(input_tokens, output_tokens, input_price, output_price):

    input_cost = (input_tokens * input_price) / 1_000_000

    output_cost = (output_tokens * output_price) / 1_000_000

    return input_cost + output_cost


# ---------------- GET PROMPT ----------------

if len(sys.argv) < 2:
    print('Usage: uv run tracker.py "your prompt"')
    sys.exit()

prompt = " ".join(sys.argv[1:])


# ---------------- GET PROVIDER RESPONSES ----------------

gemini_result = get_gemini_response(prompt)

groq_result = get_groq_response(prompt)


# ---------------- CALCULATE COSTS ----------------

gemini_result["input_price_per_m"] = GEMINI_INPUT_PRICE
gemini_result["output_price_per_m"] = GEMINI_OUTPUT_PRICE

gemini_result["cost_usd"] = calculate_cost(
    gemini_result["input_tokens"],
    gemini_result["output_tokens"],
    GEMINI_INPUT_PRICE,
    GEMINI_OUTPUT_PRICE
)


groq_result["input_price_per_m"] = GROQ_INPUT_PRICE
groq_result["output_price_per_m"] = GROQ_OUTPUT_PRICE

groq_result["cost_usd"] = calculate_cost(
    groq_result["input_tokens"],
    groq_result["output_tokens"],
    GROQ_INPUT_PRICE,
    GROQ_OUTPUT_PRICE
)


# ---------------- DISPLAY RESPONSES ----------------

print("\n--- GEMINI RESPONSE ---")
print(gemini_result["reply"])

print("\n--- GROQ RESPONSE ---")
print(groq_result["reply"])


# ---------------- COMPARISON TABLE ----------------

print("\n--- PROVIDER COMPARISON ---")

print(
    f"{'Provider':<12}"
    f"{'Input Tokens':<16}"
    f"{'Output Tokens':<17}"
    f"{'Seconds':<12}"
    f"{'Cost (USD)':<15}"
)

print("-" * 72)

for result in [gemini_result, groq_result]:

    print(
        f"{result['provider']:<12}"
        f"{result['input_tokens']:<16}"
        f"{result['output_tokens']:<17}"
        f"{result['elapsed_seconds']:<12.2f}"
        f"${result['cost_usd']:<14.8f}"
    )


# ---------------- SAVE RESULTS TO JSON ----------------

gemini_result.pop("elapsed_seconds")
groq_result.pop("elapsed_seconds")

if os.path.exists("results.json"):
    with open("results.json", "r") as file:
        results = json.load(file)
else:
    results = []

results.append(gemini_result)
results.append(groq_result)

with open("results.json", "w") as file:
    json.dump(results, file, indent=4)

print("\nResults saved to results.json")
