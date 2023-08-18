from django.core.exceptions import ValidationError

def subject_verb_not_equal(value):
 
    if subject == verb:
        raise ValidationError("Can't have both fields equal")