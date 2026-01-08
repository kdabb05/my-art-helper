"""Art Helper web app built with Reflex."""
import reflex as rx
from art_helper.pages.index import index
from art_helper.state import ArtHelperState

# Create app
app = rx.App()

# Add index page to root route
app.add_page(index, route="/", title="Art Helper")
