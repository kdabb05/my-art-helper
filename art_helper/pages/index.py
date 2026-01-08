"""Pages for Art Helper web app."""
import reflex as rx
from art_helper.state import ArtHelperState


def index() -> rx.Component:
    """Main page with dropdown and results."""
    return rx.container(
        rx.vstack(
            rx.heading("Art Helper", size="8"),
            rx.text("Select an art medium to get material suggestions from an AI instructor."),
            
            # Dropdown for medium selection
            rx.vstack(
                rx.text("Select Your Medium:", weight="bold"),
                rx.select(
                    value=ArtHelperState.selected_medium,
                    on_change=ArtHelperState.set_selected_medium,
                    items=["watercolor", "acrylic", "markers", "colored pencils", "oil"],
                ),
                spacing="2",
            ),
            
            # Submit button
            rx.button(
                "Get Suggestions",
                on_click=ArtHelperState.fetch_materials,
                is_loading=ArtHelperState.is_loading,
                width="100%",
                margin_top="1em",
            ),
            
            # Error message
            rx.cond(
                ArtHelperState.error_message != "",
                rx.box(
                    rx.text(ArtHelperState.error_message, color="red.600"),
                    border_left="4px solid red",
                    padding="4",
                    margin_top="1em",
                    background_color="red.50",
                ),
            ),
            
            # Results display
            rx.cond(
                ArtHelperState.response != "",
                rx.box(
                    rx.text(ArtHelperState.response, white_space="pre-wrap"),
                    border_width="1px",
                    border_color="gray.200",
                    padding="4",
                    border_radius="md",
                    margin_top="2em",
                    background_color="gray.50",
                ),
            ),
            
            spacing="4",
            padding="2em",
            max_width="600px",
            margin="0 auto",
        ),
        center_content=True,
    )
