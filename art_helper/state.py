"""State management for Art Helper web app."""
import os
import reflex as rx
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class ArtHelperState(rx.State):
    """State class for Art Helper."""

    mediums: list[str] = [
        "watercolor",
        "acrylic",
        "markers",
        "colored pencils",
        "oil",
    ]
    
    selected_medium: str = ""
    response: str = ""
    is_loading: bool = False
    error_message: str = ""

    def build_prompt(self, medium: str) -> str:
        """Build structured prompt for LLM."""
        return (
            f"You are an expert art instructor. The user selected the medium '{medium}'.\n"
            "Provide four clear sections with headings:\n"
            "1) Essential Materials: a concise bullet list of must-have items.\n"
            "2) Practical Tips: a short section with actionable tips for using those materials effectively.\n"
            "3) Budget Upgrades: list inexpensive/budget-friendly alternatives.\n"
            "4) Nice-to-Have Upgrades: premium upgrades worth considering.\n"
            "Keep responses short and practical. Use plain text headings exactly as: 'Essential Materials:', 'Practical Tips:', 'Budget Upgrades:', 'Nice-to-Have Upgrades:'."
        )

    async def fetch_materials(self):
        """Fetch materials from OpenRouter API based on selected medium."""
        if not self.selected_medium:
            self.error_message = "Please select a medium first."
            return

        self.is_loading = True
        self.response = ""
        self.error_message = ""

        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                self.error_message = "ERROR: OPENAI_API_KEY not set. See README.md for setup."
                self.is_loading = False
                return

            api_base = os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1")
            model = os.getenv("OPENAI_MODEL", "mistralai/mistral-small-creative")

            prompt = self.build_prompt(self.selected_medium)
            client = OpenAI(api_key=api_key, base_url=api_base)
            
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.7,
            )
            
            content = response.choices[0].message.content
            if content:
                self.response = content.strip()
            else:
                self.error_message = "API response content is empty."
        except Exception as e:
            self.error_message = f"API call failed: {str(e)}"
        finally:
            self.is_loading = False

    def set_selected_medium(self, medium: str):
        """Set the selected medium and trigger reactivity."""
        self.selected_medium = medium
        self.dirty("selected_medium")  # Mark the state as dirty to ensure reactivity
