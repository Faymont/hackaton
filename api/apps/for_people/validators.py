from django.core.validators import BaseValidator, ValidationError
from django.utils.translation import gettext_lazy as _
from jsonschema import validate, ValidationError as JSValidationError

DIGIT_JSON_FIELD_SCHEMA = {
    "type": "object",
    'additionalProperties': {'type': 'number'}
}


class JSONSchemaValidator(BaseValidator):
    """ Проверка значений объекта на числа. """
    def compare(self, a, b):
        try:
            validate(a, b)
        except JSValidationError:
            raise ValidationError(_('Значения могут быть только числовыми.'))
