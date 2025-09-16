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
        {"id": "archivos", "label": "Archivos", "icon": "📁"},
        {"id": "tasks", "label": "Tareas", "icon": "✅"},
        {"id": "team", "label": "Equipo", "icon": "👥"},
        {"id": "settings", "label": "Configuración", "icon": "⚙️"},
        {"id": "reports", "label": "Reportes", "icon": "📋"},
        {"id": "calendar", "label": "Calendario", "icon": "📅"},
    ]
    
    # Colores disponibles para resaltar el título de página
    available_colors: List[str] = [
        "#6366f1", "#8b5cf6", "#06b6d4", "#10b981", 
        "#f59e0b", "#ef4444", "#ec4899", "#14b8a6",
        "#8b5cf6", "#f97316", "#84cc16", "#3b82f6",
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
            "archivos": [
                {"id": "importar_actividades", "label": "Importar actividades CRM", "type": "page"},
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


class ImportState(rx.State):
    """Maneja la importación de actividades desde Excel."""

    is_importing: bool = False
    last_result_message: str = ""
    # Clave para forzar el remount del componente upload tras cada importación
    upload_key: int = 0
    # Flag para controlar si mostrar el mensaje
    show_result_message: bool = False

    def reset_feedback(self):
        """Limpia mensajes y estados para permitir nuevas importaciones."""
        self.is_importing = False
        self.last_result_message = ""
        self.show_result_message = False
        self.upload_key += 1  # Forzar remount del upload component

    async def import_actividades_from_upload(self, files: list[rx.UploadFile]):
        """Procesa el archivo subido y realiza la importación.

        Espera uno (1) archivo .xls/.xlsx y persiste los datos en SQLite.
        """
        if not files:
            self.last_result_message = "No se seleccionó ningún archivo."
            self.show_result_message = True
            return

        file = files[0]
        # Algunas versiones exponen .name en lugar de .filename
        filename = getattr(file, "filename", None) or getattr(file, "name", None) or "archivo.xlsx"

        # Guardar temporalmente el archivo en disco para pasarlo a openpyxl
        # Reflex expone file.read() async
        from pathlib import Path
        import tempfile

        # Solo permitir extensiones esperadas
        allowed_ext = {".xls", ".xlsx"}
        ext = Path(filename).suffix.lower()
        if ext not in allowed_ext:
            self.last_result_message = "Formato no soportado. Selecciona .xls o .xlsx"
            self.show_result_message = True
            return

        self.is_importing = True
        try:
            data = await file.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                tmp.write(data)
                tmp_path = tmp.name

            # Ejecutar importación
            from utils.xls_import_crm import import_actividades_from_excel

            inserted = import_actividades_from_excel(tmp_path)
            self.last_result_message = f"Importación completada. Registros insertados: {inserted}."
            self.show_result_message = True
        except Exception as e:
            self.last_result_message = f"Error en importación: {str(e)}"
            self.show_result_message = True
        finally:
            self.is_importing = False
            # Forzar que el componente de subida se remonte y limpie archivos previos
            self.upload_key += 1


class ImportDialogState(rx.State):
    """Estado para controlar la apertura del diálogo de importación."""

    open: bool = False

    def open_dialog(self):
        """Abre el diálogo y resetea el estado de importación."""
        # Resetear estado de importación
        yield ImportState.reset_feedback
        # Abrir el diálogo
        self.open = True

    def close_dialog(self):
        # Al cerrar el diálogo
        self.open = False

    # Setter explícito para compatibilidad futura (evita reliance en auto-setters)
    def set_open(self, value: bool):
        self.open = bool(value)

    def on_open_change(self, value: bool):
        """Controla apertura/cierre del diálogo desde el UI.

        - Al abrir, limpia mensajes/estados de importación
        - Ajusta el flag `open` según el valor recibido
        """
        self.open = bool(value)
        if value:
            # Al abrir, resetear el estado de importación usando yield
            yield ImportState.reset_feedback


