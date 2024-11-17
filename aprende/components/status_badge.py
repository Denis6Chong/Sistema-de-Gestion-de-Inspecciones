import reflex as rx

def _badge(status: str):
    badge_mapping = {
        "Cumplida": ("check", "Cumplida", "green"),
        "En Espera": ("loader", "En Espera", "yellow"),
        "No Cumplida": ("ban", "No Cumplida", "red"),
    }
    icon, text, color_scheme = badge_mapping.get(status, ("loader", "En Espera", "yellow"))
    return rx.badge(
        rx.icon(icon, size=16),
        text,
        color_scheme=color_scheme,
        radius="large",
        variant="surface",
        size="2",
    )

def status_badge(status: str):
    return rx.match(
        status,
        ("Cumplida", _badge("Cumplida")),
        ("En Espera", _badge("En Espera")),
        ("No Cumplida", _badge("No Cumplida")),
        _badge("En Espera"),
    )