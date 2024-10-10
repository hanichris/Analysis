from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='mask_num', is_safe=True)
@stringfilter
def redact_phone_number(value: str, arg: str = '*') -> str:
    """Redacts the value using the given argument.

    Hides the peronsally identifiable information (PII - phone) of a user using
    the provided redaction string that serves to obfuscate the PII.
    Args:
        value: PII to be obfuscated.
        arg: redaction string by which the PII will be obfuscated.
    Returns:
        str: Redacted string.
    """
    display = value.strip()[-3:]
    return f"{arg*5}{display}"

@register.filter(name='mask_pwd', is_safe=True)
@stringfilter
def redact_password(value: str, arg: str = '•') -> str:
    """Obfuscates the value using the provided argument `arg`.

    Hides the peronsally identifiable information (PII - password) of a user using
    the provided redaction string that serves to obfuscate the PII.
    Args:
        value: PII to be obfuscated.
        arg: redaction string by which the PII will be obfuscated.
    Returns:
        str: Redacted string.
    """
    return (arg*16).strip()