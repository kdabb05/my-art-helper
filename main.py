#!/usr/bin/env python3
import os
import sys
import argparse
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


MEDIUMS = [
    "watercolor",
    "acrylic",
    "markers",
    "colored pencils",
    "oil",
]


def choose_medium():
    print("Choose an art medium:")
    for i, m in enumerate(MEDIUMS, start=1):
        print(f"  {i}. {m}")

    while True:
        choice = input("Enter number (or name): ").strip()
        if not choice:
            continue
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(MEDIUMS):
                return MEDIUMS[idx]
        else:
            low = choice.lower()
            if low in MEDIUMS:
                return low
        print("Invalid choice — try again.")


def build_prompt(medium: str) -> str:
    return (
        f"You are an expert art instructor. The user selected the medium '{medium}'.\n"
        "Provide three clear sections with headings:\n"
        "1) Essential Materials: a concise bullet list of must-have items.\n"
        "2) Practical Tips: a short section with actionable tips for using those materials effectively.\n"
        "3) Budget vs Nice-to-Have Upgrades: list inexpensive/budget-friendly alternatives and separate 'nice-to-have' upgrades.\n"
        "Keep responses short and practical so they print cleanly in a terminal. Use plain text headings exactly as: 'Essential Materials:', 'Practical Tips:', 'Budget Upgrades:', 'Nice-to-Have Upgrades:'."
    )


def call_openrouter(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set. See README.md for setup.")
        sys.exit(1)

    api_base = os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1")
    model = os.getenv("OPENAI_MODEL", "mistralai/mistral-small-creative")

    debug = os.getenv("DEBUG_OPENAI", "false").lower() in ("1", "true", "yes")
    if debug:
        print("[debug] API base:", api_base)
        print("[debug] model:", model)
        print("[debug] using api key:", _mask_key(api_key))

    try:
        client = OpenAI(api_key=api_key, base_url=api_base)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("API call failed:", str(e))
        sys.exit(1)


def _mask_key(k: str | None) -> str:
    if not k:
        return "(none)"
    if len(k) <= 10:
        return k[0:2] + "..." + k[-2:]
    return k[:6] + "..." + k[-4:]




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mock', action='store_true', help='Run using a canned mock response (no network)')
    args = parser.parse_args()

    medium = choose_medium()
    prompt = build_prompt(medium)
    print(f"\nRequesting suggestions for: {medium}\n")

    if args.mock:
        # simple canned response for offline/testing
        reply = (
            "Essential Materials:\n- Paints\n- Brushes\n\n"
            "Practical Tips:\n- Start light, build up layers\n\n"
            "Budget Upgrades:\n- Student-grade paint set\n\n"
            "Nice-to-Have Upgrades:\n- Professional brush set"
        )
    else:
        reply = call_openrouter(prompt)

    print("=== Art Helper — Results ===\n")
    print(reply)
    print("\n=== End ===")


if __name__ == "__main__":
    print("apibas", os.getenv("OPENAI_API_BASE"))
    main()
