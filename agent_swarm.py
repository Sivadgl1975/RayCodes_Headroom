import sys
import json
import requests
from headroom import SmartCrusher
from headroom.transforms.smart_crusher import strip_ccr_sentinels

def call_ollama(model, prompt):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, timeout=600)
        response.raise_for_status()
        return response.json()["message"]["content"]
    except Exception as e:
        print(f"Error communicating with local Ollama service for model '{model}': {e}")
        print("Please ensure Ollama is running (`ollama serve`) and the model is pulled.")
        sys.exit(1)

def extract_json_array(text):
    text = text.strip()
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("[") and part.endswith("]"):
                return part
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        return text[start:end+1]
    return text

def main():
    print("🚀 Swarm Started: Executing Phase 1...")
    exec_prompt = (
        "Build a high-throughput transaction handler with data processing using Python. "
        "Generate a verbose, highly detailed technical architecture plan. "
        "Format your entire response strictly as a JSON array of objects, "
        "where each object has 'component' and 'details' keys. Do not include any markdown "
        "formatting or code fences. Output only the raw JSON."
    )
    raw_output = call_ollama("minicpm5:1b", exec_prompt)
    print("✨ Executor output received.")

    json_array_str = extract_json_array(raw_output)
    try:
        json.loads(json_array_str)
    except Exception:
        paragraphs = [p.strip() for p in raw_output.split("\n\n") if p.strip()]
        json_array_str = json.dumps([{"component": f"Section {i+1}", "details": p} for i, p in enumerate(paragraphs)])

    print("\n⚡ Compressing context with headroom-ai (strategy: smart_crusher)...")
    compressor = SmartCrusher()
    result = compressor.crush(json_array_str)
    
    try:
        compressed_items = json.loads(result.compressed)
        clean_items = strip_ccr_sentinels(compressed_items)
        compressed_output = json.dumps(clean_items, indent=2)
    except Exception:
        compressed_output = result.compressed

    raw_words = len(raw_output.split())
    comp_words = len(compressed_output.split())
    raw_tokens = int(raw_words * 1.3)
    comp_tokens = int(comp_words * 1.3)
    savings = max(0, raw_tokens - comp_tokens)
    pct_savings = (savings / raw_tokens) * 100 if raw_tokens > 0 else 0

    print(f"  - Original Context: ~{raw_tokens} tokens")
    print(f"  - Compressed Context: ~{comp_tokens} tokens")
    print(f"  - Context Compression Ratio: {pct_savings:.1f}%")

    print("\n🔍 Executing Phase 3: Reviewing compressed context...")
    review_prompt = f"Review the following compressed architecture plan for bugs and security flaws:\n\n{compressed_output}"
    review_output = call_ollama("granite4.1:3b", review_prompt)
    print("✨ Reviewer output received.")

    with open("output.md", "w", encoding="utf-8") as f:
        f.write("# Swarm Execution Report\n\n")
        f.write("## Phase 1: Raw Executor Output (minicpm5:1b)\n\n")
        f.write(f"{raw_output}\n\n")
        f.write("## Phase 2: Compressed Context (smart_crusher)\n\n")
        f.write(f"{compressed_output}\n\n")
        f.write("## Phase 3: Reviewer Output (granite4.1:3b)\n\n")
        f.write(f"{review_output}\n\n")
        f.write("## Savings Metrics\n\n")
        f.write(f"- **Raw Tokens (est.)**: {raw_tokens}\n")
        f.write(f"- **Compressed Tokens (est.)**: {comp_tokens}\n")
        f.write(f"- **Token Savings**: {savings} ({pct_savings:.1f}%)\n")

    print("\n🎉 Report saved successfully to 'output.md'. Swarm process finished.")

if __name__ == "__main__":
    main()

