from django import template

from doctors.models import Speciality

register = template.Library()


@register.inclusion_tag("partials/navbar.html")
def specialities_navbar():
    return {
        "specialities": Speciality.objects.all()
    }
