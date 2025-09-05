"""Estado principal de la aplicación."""

import reflex as rx
import random
from typing import Dict, List, Optional

class AppState(rx.State):
    """Estado principal de la aplicación que maneja navegación y UI."""
    
    # Estado del menú principal
    active_menu_item: str = ""
    
    # Estado del submenú
    submenu_open: bool = False
    submenu_items: List[Dict[str, str]] = []
    
    # Estado del área de trabajo
    current_page: str = "home"
    page_title: str = "Página en construcción"
    text_color: str = "#6366f1"
    
    # Datos del menú principal (generados aleatoriamente)
    menu_items: List[Dict[str, str]] = [
        {"id": "dashboard", "label": "Dashboard", "icon": "📊"},
        {"id": "analytics", "label": "Analytics", "icon": "📈"},
        {"id": "projects", "label": "Proyectos", "icon": "📁"},
        {"id": "tasks", "label": "Tareas", "icon": "✅"},
        {"id": "team", "label": "Equipo", "icon": "👥"},
        {"id": "settings", "label": "Configuración", "icon": "⚙️"},
        {"id": "reports", "label": "Reportes", "icon": "📋"},
        {"id": "calendar", "label": "Calendario", "icon": "📅"},
    ]
    
    def __init__(self):
        super().__init__()
        # Generar colores aleatorios disponibles
        self.available_colors = [
            "#6366f1", "#8b5cf6", "#06b6d4", "#10b981", 
            "#f59e0b", "#ef4444", "#ec4899", "#14b8a6",
            "#8b5cf6", "#f97316", "#84cc16", "#3b82f6"
        ]
    
    def toggle_submenu(self, menu_id: str):
        """Alternar visibilidad del submenú."""
        if self.active_menu_item == menu_id and self.submenu_open:
            # Si el mismo menú está activo y abierto, cerrarlo
            self.submenu_open = False
        else:
            # Abrir nuevo submenú o cambiar al seleccionado
            self.active_menu_item = menu_id
            self.submenu_open = True
            self.generate_submenu_items(menu_id)
    
    def generate_submenu_items(self, menu_id: str):
        """Generar elementos del submenú de forma aleatoria."""
        submenu_options = {
            "dashboard": [
                {"id": "overview", "label": "Vista General", "type": "page"},
                {"id": "metrics", "label": "Métricas", "type": "page"},
                {"id": "widgets", "label": "Widgets", "type": "page"},
                {"id": "filter_date", "label": "Filtrar por fecha", "type": "input"},
            ],
            "analytics": [
                {"id": "visitors", "label": "Visitantes", "type": "page"},
                {"id": "conversions", "label": "Conversiones", "type": "page"},
                {"id": "revenue", "label": "Ingresos", "type": "page"},
                {"id": "period", "label": "Período de análisis", "type": "select"},
            ],
            "projects": [
                {"id": "active", "label": "Proyectos Activos", "type": "page"},
                {"id": "completed", "label": "Completados", "type": "page"},
                {"id": "archived", "label": "Archivados", "type": "page"},
                {"id": "search", "label": "Buscar proyecto", "type": "input"},
            ],
            "tasks": [
                {"id": "pending", "label": "Pendientes", "type": "page"},
                {"id": "in_progress", "label": "En Progreso", "type": "page"},
                {"id": "completed", "label": "Completadas", "type": "page"},
                {"id": "priority", "label": "Filtrar por prioridad", "type": "select"},
            ],
            "team": [
                {"id": "members", "label": "Miembros", "type": "page"},
                {"id": "roles", "label": "Roles", "type": "page"},
                {"id": "permissions", "label": "Permisos", "type": "page"},
                {"id": "search_user", "label": "Buscar usuario", "type": "input"},
            ],
            "settings": [
                {"id": "general", "label": "General", "type": "page"},
                {"id": "security", "label": "Seguridad", "type": "page"},
                {"id": "notifications", "label": "Notificaciones", "type": "page"},
                {"id": "theme", "label": "Tema", "type": "select"},
            ],
            "reports": [
                {"id": "sales", "label": "Ventas", "type": "page"},
                {"id": "performance", "label": "Rendimiento", "type": "page"},
                {"id": "custom", "label": "Personalizado", "type": "page"},
                {"id": "export_format", "label": "Formato de exportación", "type": "select"},
            ],
            "calendar": [
                {"id": "month_view", "label": "Vista Mensual", "type": "page"},
                {"id": "week_view", "label": "Vista Semanal", "type": "page"},
                {"id": "events", "label": "Eventos", "type": "page"},
                {"id": "date_range", "label": "Rango de fechas", "type": "input"},
            ],
        }
        
        self.submenu_items = submenu_options.get(menu_id, [])
    
    def navigate_to_page(self, page_id: str, page_title: str = None):
        """Navegar a una página y generar color aleatorio."""
        self.current_page = page_id
        self.page_title = page_title or "Página en construcción"
        # Generar color aleatorio para el texto
        self.text_color = random.choice(self.available_colors)
    
    def close_submenu(self):
        """Cerrar el submenú."""
        self.submenu_open = False


