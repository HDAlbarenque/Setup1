"""Aplicación web con diseño de tres áreas: Menú principal, Submenú y Área de trabajo."""

import reflex as rx
import random
from typing import Dict, List
from Setup1.state import ImportDialogState, ImportState

# Colores del tema basados en la imagen
THEME_COLORS = {
    "primary_dark": "#1e2139",
    "secondary_dark": "#2b2f4a", 
    "accent_blue": "#6366f1",
    "background_main": "#1a1d2e",
    "surface_light": "#ffffff",
    "text_primary": "#ffffff",
    "text_secondary": "#94a3b8",
    "text_dark": "#1e293b",
    "hover": "#374151",
    "border": "#374151",
}

SPACING = {
    "sm": "0.5rem",
    "md": "1rem", 
    "lg": "1.5rem",
    "xl": "2rem",
}

class State(rx.State):
    """Estado principal de la aplicación."""
    
    # Estado del menú
    active_menu_item: str = ""
    submenu_open: bool = False
    current_page: str = "home"
    page_title: str = "Página en construcción"
    text_color: str = "#6366f1"
    
    # Menú items
    menu_items: List[Dict[str, str]] = [
        {"id": "dashboard", "label": "Dashboard", "icon": "📊"},
        {"id": "archivos", "label": "Archivo", "icon": "📁"},
        {"id": "tasks", "label": "Tareas", "icon": "✅"},
        {"id": "team", "label": "Equipo", "icon": "👥"},
        {"id": "settings", "label": "Configuración", "icon": "⚙️"},
        {"id": "reports", "label": "Reportes", "icon": "📋"},
        {"id": "calendar", "label": "Calendario", "icon": "📅"},
    ]
    
    # Submenu items
    submenu_items: List[Dict[str, str]] = []
    
    available_colors: List[str] = [
        "#6366f1", "#8b5cf6", "#06b6d4", "#10b981", 
        "#f59e0b", "#ef4444", "#ec4899", "#14b8a6",
    ]
    
    def toggle_submenu(self, menu_id: str):
        """Alternar visibilidad del submenú."""
        if self.active_menu_item == menu_id and self.submenu_open:
            self.submenu_open = False
        else:
            self.active_menu_item = menu_id
            self.submenu_open = True
            self.generate_submenu_items(menu_id)
    
    def generate_submenu_items(self, menu_id: str):
        """Generar elementos del submenú."""
        submenu_options = {
            "dashboard": [
                {"id": "overview", "label": "Vista General", "type": "page"},
                {"id": "metrics", "label": "Métricas", "type": "page"},
                {"id": "widgets", "label": "Widgets", "type": "page"},
            ],
            "archivos": [
                {"id": "importar_actividades_crm", "label": "Importar actividades CRM", "type": "page", "icon": "/excel_icon.png"},
            ],
        }
        
        self.submenu_items = submenu_options.get(menu_id, [
            {"id": "item1", "label": f"Opción 1 de {menu_id}", "type": "page"},
            {"id": "item2", "label": f"Opción 2 de {menu_id}", "type": "page"},
            {"id": "item3", "label": f"Opción 3 de {menu_id}", "type": "page"},
        ])
    
    def navigate_to_page(self, page_id: str, page_title: str = "Página en construcción"):
        """Navegar a una página."""
        self.current_page = page_id
        self.page_title = page_title
        self.text_color = random.choice(self.available_colors)
    
    def close_submenu(self):
        """Cerrar el submenú."""
        self.submenu_open = False


def menu_item(item_id: str, label: str, icon: str) -> rx.Component:
    """Componente individual del menú principal."""
    return rx.box(
        rx.button(
            rx.vstack(
                rx.box(
                    rx.text(
                        icon, 
                        font_size="1.4rem", 
                        line_height="1",
                    ),
                    height="24px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.box(
                    rx.text(
                        label,
                        font_size="0.7rem",
                        font_weight="500",
                        text_align="center",
                        line_height="1",
                        white_space="nowrap",
                        overflow="hidden",
                        text_overflow="ellipsis",
                        max_width="100%",
                    ),
                    height="16px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                spacing="1",
                align="center",
                justify="center",
                width="100%",
                height="100%",
            ),
            width="100%",
            height="100%",
            padding="0.25rem",
            background_color=rx.cond(
                State.active_menu_item == item_id,
                THEME_COLORS["secondary_dark"],
                "transparent"
            ),
            color=THEME_COLORS["text_primary"],
            border="none",
            border_radius="0.75rem",
            cursor="pointer",
            transition="all 0.2s ease",
            _hover={
                "background_color": rx.cond(
                    State.active_menu_item == item_id,
                    THEME_COLORS["secondary_dark"],
                    THEME_COLORS["hover"]
                ),
                "transform": "translateY(-1px)",
            },
            _active={
                "transform": "translateY(0px)",
            },
            on_click=State.toggle_submenu(item_id),
        ),
        width="100%",
        height="70px",
        margin_bottom="0.75rem",
        flex_shrink="0",
    )


def main_menu() -> rx.Component:
    """Menú principal vertical."""
    return rx.box(
        rx.vstack(
            # Logo
            rx.box(
                rx.text("🏢", font_size="2rem", margin_bottom="0.5rem"),
                rx.text(
                    "Mi App",
                    font_size="1.125rem",
                    font_weight="700",
                    color=THEME_COLORS["text_primary"],
                ),
                text_align="center",
                padding=SPACING["md"],
                border_bottom=f"1px solid {THEME_COLORS['border']}",
                margin_bottom=SPACING["md"],
            ),
            
            # Items del menú
            rx.foreach(
                State.menu_items,
                lambda item: menu_item(item["id"], item["label"], item["icon"])
            ),
            
            spacing="0",
            width="100%",
            padding=SPACING["sm"],
            align="stretch",
        ),
        width="120px",
        min_height="100vh",
        background_color=THEME_COLORS["primary_dark"],
        border_right=f"1px solid {THEME_COLORS['border']}",
        position="fixed",
        left="0",
        top="0",
        z_index="100",
    )


def submenu_item(item: dict) -> rx.Component:
    """Componente individual del submenú."""
    return rx.button(
        rx.hstack(
            rx.cond(
                item.get("icon", ""),
                rx.cond(
                    item["icon"].startswith("/"),
                    rx.image(
                        src=item["icon"], 
                        width=rx.cond(item["id"] == "importar_actividades_crm", "1.5rem", "1rem"),
                        height=rx.cond(item["id"] == "importar_actividades_crm", "1.5rem", "1rem")
                    ),
                    rx.text(
                        item["icon"], 
                        font_size=rx.cond(item["id"] == "importar_actividades_crm", "1.5rem", "1rem")
                    ),
                ),
                rx.text(
                    "📄", 
                    font_size=rx.cond(item["id"] == "importar_actividades_crm", "1.5rem", "1rem")
                ),
            ),
            rx.text(item["label"], font_size="0.875rem", font_weight="500"),
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
        _hover={"background_color": THEME_COLORS["hover"]},
        on_click=rx.cond(
            item["id"] == "importar_actividades_crm",
            ImportDialogState.open_dialog,
            State.navigate_to_page(item["id"], item["label"]),
        ),
    )


def submenu() -> rx.Component:
    """Submenú colapsable."""
    return rx.cond(
        State.submenu_open,
        rx.box(
            rx.vstack(
                # Header del submenú
                rx.hstack(
                    rx.text(
                        "Opciones",
                        font_size="1.125rem",
                        font_weight="600",
                        color=THEME_COLORS["text_primary"],
                    ),
                    rx.button(
                        "✕",
                        size="2",
                        background_color="transparent",
                        color=THEME_COLORS["text_secondary"],
                        border="none",
                        cursor="pointer",
                        _hover={"color": THEME_COLORS["text_primary"]},
                        on_click=State.close_submenu,
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
                        State.submenu_items,
                        lambda item: submenu_item(item)
                    ),
                    width="100%",
                    padding=f"0 {SPACING['lg']}",
                ),
                
                spacing="0",
                width="100%",
            ),
            width="320px",
            min_height="100vh",
            background_color=THEME_COLORS["secondary_dark"],
            border_right=f"1px solid {THEME_COLORS['border']}",
            position="fixed",
            left="120px",
            top="0",
            z_index="90",
        ),
        rx.box(),
    )


def work_area() -> rx.Component:
    """Área de trabajo principal."""
    margin_left = rx.cond(
        State.submenu_open,
        "440px",  # 120px + 320px
        "120px"
    )
    
    return rx.box(
        rx.center(
            rx.vstack(
                rx.text(
                    State.page_title,
                    font_size="3rem",
                    font_weight="700",
                    color=State.text_color,
                    text_align="center",
                    line_height="1.2",
                ),
                rx.text(
                    f"Página actual: {State.current_page}",
                    font_size="1.125rem",
                    color=THEME_COLORS["text_secondary"],
                    text_align="center",
                    margin_top=SPACING["lg"],
                ),
                spacing="4",
                align="center",
            ),
            height="100vh",
        ),
        margin_left=margin_left,
        background_color=THEME_COLORS["background_main"],
        min_height="100vh",
        padding=SPACING["xl"],
    )


def index() -> rx.Component:
    """Layout principal de la aplicación."""
    def import_dialog():
        return rx.dialog.root(
            rx.dialog.trigger(rx.box()),
            rx.dialog.content(
                rx.vstack(
                    rx.hstack(
                        rx.text("Importar actividades", font_weight="700", font_size="1.125rem"),
                        rx.button(
                            "✕",
                            size="2",
                            background_color="transparent",
                            color=THEME_COLORS["text_secondary"],
                            border="none",
                            cursor="pointer",
                            _hover={"color": THEME_COLORS["text_primary"]},
                            on_click=ImportDialogState.close_dialog,
                        ),
                        justify="between",
                        align="center",
                        width="100%",
                    ),
                    rx.upload(
                        rx.vstack(
                            rx.icon(tag="upload"),
                            rx.text("Selecciona o suelta un archivo .xls/.xlsx"),
                            spacing="2",
                            align="center",
                        ),
                        multiple=False,
                        accept={"application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"},
                        max_files=1,
                        on_drop=ImportState.import_actividades_from_upload(rx.upload_files()),
                        key=ImportState.upload_key,
                    ),
                    rx.cond(
                        ImportState.is_importing,
                        rx.hstack(rx.spinner(), rx.text("Importando..."), spacing="2"),
                        rx.cond(
                            ImportState.show_result_message,
                            rx.text(ImportState.last_result_message, color=THEME_COLORS["text_secondary"]),
                            rx.box()  # Elemento vacío cuando no hay mensaje
                        )
                    ),
                    spacing="4",
                    width="100%",
                ),
                style={"width": "480px", "maxWidth": "90vw"},
            ),
            open=ImportDialogState.open,
            on_open_change=ImportDialogState.on_open_change,
        )

    return rx.box(
        main_menu(),
        submenu(),
        work_area(),
        import_dialog(),
        width="100%",
        height="100vh",
        overflow="hidden",
        font_family="'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    )


app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
    ]
)

app.add_page(index, route="/")