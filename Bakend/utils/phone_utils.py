""""utilidades de teléfono.
Funciones para validación y formateo de números telefónicos."""

def is_valid_phone_number(phone_number: str) -> bool:
    """Valida si el número telefónico tiene un formato correcto."""
    digits = ''.join(filter(str.isdigit, phone_number))
    #Asumimos un formato simple de 10 dígitos porque se agregar el +52 para México
    return len(digits) == 10
    
def format_phone_number(phone_number: str) -> str:
    """Formatea el número telefónico al estándar E.164 con código de país +52 (México)."""
    digits = ''.join(filter(str.isdigit, phone_number))
    if len(digits) == 10:
        return f"+52{digits}"
    raise ValueError("Número telefónico inválido para formatear.")