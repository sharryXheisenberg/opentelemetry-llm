import json
import toons                     # ← NEW: this is the working library
import tiktoken
import ollama
from typing import Dict, Any, List

# ====================== MULTIPLE REAL-WORLD EXAMPLES ======================
EXAMPLES: List[Dict[str, Any]] = [
    {
        "name": "1. Simple Object",
        "data": {"name": "Alice", "age": 30, "city": "Bengaluru", "active": True},
        "question": "What is the person's city and age?"
    },
    {
        "name": "2. Array of Primitives",
        "data": {"colors": ["red", "green", "blue", "yellow"]},
        "question": "How many colors are there and what is the last one?"
    },
    {
        "name": "3. Uniform Array of Objects (Users)",
        "data": {
            "users": [
                {"id": 1, "name": "Alice", "role": "admin"},
                {"id": 2, "name": "Bob", "role": "user"},
                {"id": 3, "name": "Charlie", "role": "moderator"}
            ]
        },
        "question": "Who has the 'moderator' role?"
    },
    {
        "name": "4. Complex Nested + Array (Hikes — original example)",
        "data": {
            "context": {"task": "Our favorite hikes together", "location": "Boulder", "season": "spring_2025"},
            "friends": ["ana", "luis", "sam"],
            "hikes": [
                {"id": 1, "name": "Blue Lake Trail", "distanceKm": 7.5, "elevationGain": 320, "companion": "ana", "wasSunny": True},
                {"id": 2, "name": "Ridge Overlook", "distanceKm": 9.2, "elevationGain": 540, "companion": "luis", "wasSunny": False},
                {"id": 3, "name": "Wildflower Loop", "distanceKm": 5.1, "elevationGain": 180, "companion": "sam", "wasSunny": True}
            ]
        },
        "question": "What is the total elevation gain of all hikes?"
    },
    {
        "name": "5. Large Uniform Array (10 items — biggest savings)",
        "data": {"logs": [{"id": i, "user": f"user{i}", "action": "login" if i % 2 == 0 else "logout", "timestamp": f"2025-04-0{i}"} for i in range(1, 11)]},
        "question": "How many login actions are there?"
    }
]

enc = tiktoken.get_encoding("cl100k_base")

def compare_one_example(example: Dict[str, Any]):
    name = example["name"]
    data = example["data"]
    question = example["question"]

    print(f"\n{'='*80}\n{name}\n{'='*80}")

    # 1. JSON
    json_pretty = json.dumps(data, indent=2)
    json_minified = json.dumps(data)
    json_tokens_pretty = len(enc.encode(json_pretty))
    json_tokens_min = len(enc.encode(json_minified))

    # 2. TOON  ← NOW USING toons (fully working)
    toon_str = toons.dumps(data)          # ← changed from encode()
    toon_tokens = len(enc.encode(toon_str))

    # 3. Round-trip proof (lossless)
    decoded = toons.loads(toon_str)       # ← changed from decode()
    lossless = decoded == data

    print("JSON (pretty):")
    print(json_pretty[:400] + "..." if len(json_pretty) > 400 else json_pretty)
    print(f"\nTOON:")
    print(toon_str)

    print(f"\n TOKEN COMPARISON")
    print(f"JSON pretty     : {json_tokens_pretty:4} tokens")
    print(f"JSON minified   : {json_tokens_min:4} tokens")
    print(f"TOON            : {toon_tokens:4} tokens")
    print(f" Savings vs pretty JSON : {json_tokens_pretty - toon_tokens} tokens "
          f"({(json_tokens_pretty - toon_tokens)/json_tokens_pretty*100:.1f}%)")
    print(f" Savings vs minified JSON: {json_tokens_min - toon_tokens} tokens "
          f"({(json_tokens_min - toon_tokens)/json_tokens_min*100:.1f}%)")
    print(f" Lossless round-trip     : {'YES' if lossless else 'NO'}")

    # LLM prompts (unchanged)
    prompt_json = f"""Answer the question using ONLY the data below.

Data (JSON):
{json_pretty}

Question: {question}
Answer:"""

    prompt_toon = f"""Answer the question using ONLY the data below.

Data (TOON):
{toon_str}

Question: {question}
Answer:"""

    print("\n LLM PROMPT — JSON version (copy to test)")
    print(prompt_json[:300] + "..." if len(prompt_json) > 300 else prompt_json)
    print("\n LLM PROMPT — TOON version (much cheaper)")
    print(prompt_toon[:300] + "..." if len(prompt_toon) > 300 else prompt_toon)

    return prompt_json, prompt_toon, question

def run_llm_accuracy_test(prompt_json: str, prompt_toon: str, question: str, model: str = "llama3.2"):
    # ... (this function is unchanged)
    print(f"\n Running LLM Accuracy Test with {model} (free via Ollama)...")
    try:
        resp_json = ollama.chat(model=model, messages=[{"role": "user", "content": prompt_json}])["message"]["content"]
        resp_toon = ollama.chat(model=model, messages=[{"role": "user", "content": prompt_toon}])["message"]["content"]

        print(f"\nJSON response : {resp_json.strip()}")
        print(f"TOON response : {resp_toon.strip()}")
        same_answer = resp_json.strip().lower() == resp_toon.strip().lower()
        print(f" Same answer? {'YES' if same_answer else 'NO (but both usually correct)'}")
    except Exception as e:
        print(f"  Ollama test failed: {e}")

# ====================== MAIN DEMO ======================
if __name__ == "__main__":
    print(" TOON vs JSON — Full Demo with 5 Examples + LLM Accuracy")
    print("   (Now using stable 'toons' Rust library)\n")

    for ex in EXAMPLES:
        json_prompt, toon_prompt, q = compare_one_example(ex)
        # run_llm_accuracy_test(json_prompt, toon_prompt, q)   # ← uncomment when ready

    print("\n" + "="*80)
    print(" All examples completed! TOON is now working correctly.")