from django import template

register = template.Library()


@register.inclusion_tag("accounts/patient_appointments.html", takes_context=True)
def appointments(context):
    """
    This function is a Django template inclusion tag that retrieves all specialities from the database
    and passes them to the "accounts/templates/patient_appointments.html" template for rendering.

    Parameters:
    None

    Returns:
    A dictionary containing the following key-value pairs:
        - specialities: A QuerySet of all Speciality objects retrieved from the database.

    Example usage:
    ```python
    {% load appointments %}
    ```
    """
    appos = context["appointments"]
    attended = appos["attended"]
    not_attended = appos["not_attended"]
    return {
        "attended": attended,
        "not_attended": not_attended,
    }
