from django import template

from doctors.models import Speciality

register = template.Library()


@register.inclusion_tag("partials/navbar.html")
def navbar():
    """
    This function is a Django template inclusion tag that retrieves all specialities from the database
    and passes them to the "partials/navbar.html" template for rendering.

    Parameters:
    None

    Returns:
    A dictionary containing the following key-value pairs:
        - specialities: A QuerySet of all Speciality objects retrieved from the database.

    Example usage:
    ```python
    {% specialities %}
    ```
    """
    return {"specialities": Speciality.objects.all()}
