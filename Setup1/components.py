"""Componentes de UI para la aplicación."""

import reflex as rx
from .theme import THEME_COLORS, SPACING, LAYOUT_DIMENSIONS, TYPOGRAPHY, EFFECTS
from .state import AppState


def menu_item(item_id: str, label: str, icon: str) -> rx.Component:
    """Componente individual del menú principal."""
    return rx.button(
        rx.vstack(
            rx.text(
                icon,
                font_size="1.5rem",
                margin_bottom="0.25rem",
            ),
            rx.text(
                label,
                font_size=TYPOGRAPHY["font_sizes"]["xs"],
                font_weight="500",
                text_align="center",
                line_height="1.2",
            ),
            spacing="1",
            align="center",
            width="100%",
        ),
        width="100%",
        padding=SPACING["md"],
        background_color=rx.cond(
            AppState.active_menu_item == item_id,
            THEME_COLORS["accent_blue"],
            "transparent"
        ),
        color=THEME_COLORS["text_primary"],
        border="none",
        border_radius=EFFECTS["border_radius"],
        cursor="pointer",
        transition=EFFECTS["transition"],
        _hover={
            "background_color": rx.cond(
                AppState.active_menu_item == item_id,
                THEME_COLORS["accent_blue"],
                THEME_COLORS["hover"]
            ),
            "transform": "scale(1.05)",
        },
        on_click=AppState.toggle_submenu(item_id),
    )


def main_menu() -> rx.Component:
    """Menú principal vertical del lado izquierdo."""
    return rx.box(
        rx.vstack(
            # Logo o título
            rx.box(
                rx.text(
                    "🏢",
                    font_size="2rem",
                    margin_bottom="0.5rem",
                ),
                rx.text(
                    "Mi App",
                    font_size=TYPOGRAPHY["font_sizes"]["lg"],
                    font_weight="700",
                    color=THEME_COLORS["text_primary"],
                ),
                text_align="center",
                padding=SPACING["lg"],
                border_bottom=f"1px solid {THEME_COLORS['border']}",
                margin_bottom=SPACING["lg"],
            ),
            
            # Items del menú
            rx.foreach(
                AppState.menu_items,
                lambda item: menu_item(
                    item["id"],
                    item["label"], 
                    item["icon"]
                )
            ),
            
            spacing="2",
            width="100%",
            padding=SPACING["md"],
        ),
        width=LAYOUT_DIMENSIONS["sidebar_width"],
        min_height=LAYOUT_DIMENSIONS["min_height"],
        background_color=THEME_COLORS["primary_dark"],
        border_right=f"1px solid {THEME_COLORS['border']}",
        position="fixed",
        left="0",
        top="0",
        z_index="100",
    )


def submenu_item(item_id: str, label: str, item_type: str) -> rx.Component:
    """Componente individual del submenú."""
    if item_type == "input":
        return rx.box(
            rx.text(
                label,
                font_size=TYPOGRAPHY["font_sizes"]["sm"],
                color=THEME_COLORS["text_secondary"],
                margin_bottom="0.5rem",
            ),
            rx.input(
                placeholder=f"Ingrese {label.lower()}",
                width="100%",
                background_color=THEME_COLORS["surface_card"],
                border=f"1px solid {THEME_COLORS['border']}",
                border_radius="0.5rem",
                padding=SPACING["sm"],
            ),
            margin_bottom=SPACING["md"],
        )
    elif item_type == "select":
        return rx.box(
            rx.text(
                label,
                font_size=TYPOGRAPHY["font_sizes"]["sm"],
                color=THEME_COLORS["text_secondary"],
                margin_bottom="0.5rem",
            ),
            rx.select(
                ["Opción 1", "Opción 2", "Opción 3"],
                placeholder=f"Seleccione {label.lower()}",
                width="100%",
                background_color=THEME_COLORS["surface_card"],
                border=f"1px solid {THEME_COLORS['border']}",
                border_radius="0.5rem",
            ),
            margin_bottom=SPACING["md"],
        )
    else:  # page type
        return rx.button(
            rx.hstack(
                rx.text("📄", font_size="1rem"),
                rx.text(
                    label,
                    font_size=TYPOGRAPHY["font_sizes"]["sm"],
                    font_weight="500",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            width="100%",
            padding=SPACING["md"],
            background_color="transparent",
            color=THEME_COLORS["text_primary"],
            border="none",
            border_radius="0.5rem",
            cursor="pointer",
            text_align="left",
            justify_content="flex-start",
            _hover={
                "background_color": THEME_COLORS["hover"],
            },
            on_click=AppState.navigate_to_page(item_id, label),
        )


def submenu() -> rx.Component:
    """Submenú colapsable."""
    return rx.cond(
        AppState.submenu_open,
        rx.box(
            rx.vstack(
                # Header del submenú
                rx.hstack(
                    rx.text(
                        "Filtros y Opciones",
                        font_size=TYPOGRAPHY["font_sizes"]["lg"],
                        font_weight="600",
                        color=THEME_COLORS["text_primary"],
                    ),
                    rx.button(
                        "✕",
                        size="sm",
                        background_color="transparent",
                        color=THEME_COLORS["text_secondary"],
                        border="none",
                        cursor="pointer",
                        _hover={"color": THEME_COLORS["text_primary"]},
                        on_click=AppState.close_submenu,
                    ),
                    justify="between",
                    align="center",
                    width="100%",
                    padding=SPACING["lg"],
                    border_bottom=f"1px solid {THEME_COLORS['border']}",
                    margin_bottom=SPACING["lg"],
                ),
                
                # Items del submenú
                rx.box(
                    rx.foreach(
                        AppState.submenu_items,
                        lambda item: submenu_item(
                            item["id"],
                            item["label"],
                            item["type"]
                        )
                    ),
                    width="100%",
                    padding=f"0 {SPACING['lg']}",
                ),
                
                spacing="0",
                width="100%",
            ),
            width=LAYOUT_DIMENSIONS["submenu_width"],
            min_height=LAYOUT_DIMENSIONS["min_height"],
            background_color=THEME_COLORS["secondary_dark"],
            border_right=f"1px solid {THEME_COLORS['border']}",
            position="fixed",
            left=LAYOUT_DIMENSIONS["sidebar_width"],
            top="0",
            z_index="90",
            # animation="slideIn 0.3s ease",
        ),
        rx.box(),  # Elemento vacío cuando está cerrado
    )


def work_area() -> rx.Component:
    """Área de trabajo principal."""
    margin_left = rx.cond(
        AppState.submenu_open,
        f"calc({LAYOUT_DIMENSIONS['sidebar_width']} + {LAYOUT_DIMENSIONS['submenu_width']})",
        LAYOUT_DIMENSIONS["sidebar_width"]
    )
    
    return rx.box(
        rx.center(
            rx.vstack(
                rx.text(
                    AppState.page_title,
                    font_size=TYPOGRAPHY["font_sizes"]["5xl"],
                    font_weight="700",
                    color=AppState.text_color,
                    text_align="center",
                    line_height="1.2",
                ),
                rx.text(
                    f"Página actual: {AppState.current_page}",
                    font_size=TYPOGRAPHY["font_sizes"]["lg"],
                    color=THEME_COLORS["text_muted"],
                    text_align="center",
                    margin_top=SPACING["lg"],
                ),
                spacing="4",
                align="center",
            ),
            height="100vh",
        ),
        margin_left=margin_left,
        background_color=THEME_COLORS["surface_light"],
        min_height=LAYOUT_DIMENSIONS["min_height"],
        padding=SPACING["xl"],
        transition=EFFECTS["transition"],
    )


def app_layout() -> rx.Component:
    """Layout principal de la aplicación."""
    return rx.box(
        main_menu(),
        submenu(),
        work_area(),
        width="100%",
        height="100vh",
        overflow="hidden",
        font_family=TYPOGRAPHY["font_family"],
    )
