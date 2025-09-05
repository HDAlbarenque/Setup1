"""Sistema de colores y tema basado en el diseño de referencia."""

# Colores extraídos de la imagen de referencia
THEME_COLORS = {
    # Colores principales del diseño oscuro
    "primary_dark": "#1e2139",      # Azul oscuro principal del sidebar
    "secondary_dark": "#2b2f4a",    # Azul oscuro secundario
    "accent_blue": "#6366f1",       # Azul vibrante para elementos activos
    "accent_purple": "#8b5cf6",     # Púrpura para elementos destacados
    
    # Colores de fondo y superficie
    "background_main": "#1a1d2e",   # Fondo principal de la app
    "surface_light": "#ffffff",     # Superficie clara (área de trabajo)
    "surface_card": "#f8fafc",      # Fondo de tarjetas
    
    # Colores de texto
    "text_primary": "#ffffff",      # Texto principal en áreas oscuras
    "text_secondary": "#94a3b8",    # Texto secundario
    "text_dark": "#1e293b",         # Texto en áreas claras
    "text_muted": "#64748b",        # Texto menos importante
    
    # Estados y elementos interactivos
    "success": "#10b981",           # Verde para éxito
    "warning": "#f59e0b",           # Amarillo para advertencias
    "error": "#ef4444",             # Rojo para errores
    "hover": "#374151",             # Color de hover
    
    # Bordes y divisores
    "border": "#374151",            # Bordes sutiles
    "divider": "#4b5563",           # Líneas divisorias
}

# Sistema de espaciado (8px base)
SPACING = {
    "xs": "0.25rem",   # 4px
    "sm": "0.5rem",    # 8px
    "md": "1rem",      # 16px
    "lg": "1.5rem",    # 24px
    "xl": "2rem",      # 32px
    "2xl": "3rem",     # 48px
    "3xl": "4rem",     # 64px
}

# Tipografía del sistema
TYPOGRAPHY = {
    "font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "font_sizes": {
        "xs": "0.75rem",     # 12px
        "sm": "0.875rem",    # 14px
        "base": "1rem",      # 16px
        "lg": "1.125rem",    # 18px
        "xl": "1.25rem",     # 20px
        "2xl": "1.5rem",     # 24px
        "3xl": "1.875rem",   # 30px
        "4xl": "2.25rem",    # 36px
        "5xl": "3rem",       # 48px
    }
}

# Dimensiones del layout
LAYOUT_DIMENSIONS = {
    "sidebar_width": "240px",       # Ancho del menú principal
    "submenu_width": "320px",       # Ancho del submenú
    "header_height": "64px",        # Altura del header (si se necesita)
    "min_height": "100vh",          # Altura mínima de la aplicación
}

# Efectos y transiciones
EFFECTS = {
    "transition": "all 0.3s ease",
    "hover_transform": "translateY(-2px)",
    "shadow_sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "shadow_md": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
    "shadow_lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
    "border_radius": "0.75rem",
}


