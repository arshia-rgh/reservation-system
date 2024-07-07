from django.contrib import admin

from surveys.models import Comment, Rate


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Django ModelAdmin class for Comment model.

    This class provides customizations for the Comment model in the Django admin interface.
    """

    pass


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    """
    Django ModelAdmin class for Rate model.

    This class provides customizations for the Rate model in the Django admin interface.
    """

    pass
