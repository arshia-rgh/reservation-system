from django.db.models import Q
from django.views.generic import ListView

from doctors.models import Doctor, Speciality


class IndexHomePageView(ListView):
    """
    This class represents the Index Home Page View in the Django application.
    It inherits from Django's ListView and is responsible for displaying a list of doctors.
    """

    template_name = "home/index.html"  # The template to be used for rendering the view.
    queryset = Doctor.objects.all()  # The queryset of doctors to be displayed.
    context_object_name = "doctors"  # The name of the variable to be used in the template context.

    def get_queryset(self):
        """
        This method overrides the default get_queryset method of ListView.
        It filters the queryset based on the speciality filter provided in the request query parameters.

        :return: The filtered queryset of doctors.
        """
        name_filter = self.request.GET.get(
            "name"
            ) # Get the name filter from the request query parameters.
        if name_filter :
            # If a name filter is provided, filter the queryset based on the name.
            return self.queryset.filter(
                Q(first_name__icontains=name_filter)|Q(last_name__icontains=name_filter)
            )
        speciality_filter = self.request.GET.get(
            "speciality"
        )  # Get the speciality filter from the request query parameters.
        if speciality_filter:
            # If a speciality filter is provided, filter the queryset based on the speciality.
            return self.queryset.filter(speciality__name__icontains=speciality_filter)
        return self.queryset.all()  # If no speciality filter is provided, return the original queryset.

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        speciality_filter = self.request.GET.get("speciality")
        if speciality_filter and Speciality.objects.filter(name__icontains=speciality_filter).exists():
            context["speciality_filter"] = speciality_filter  # Add the speciality filter to the context.
        return context
