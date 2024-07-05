from django.db import models


class BaseModelMixin(models.Model):
    """
    This is an abstract base model class that provides common fields for all models.

    Attributes:
    created_at (DateTimeField): Automatically set to the current date and time when an object is first created.
    updated_at (DateTimeField): Automatically set to the current date and time whenever an object is saved.

    Methods:
    None
    """

    created_at = models.DateTimeField(auto_now_add=True)
    """
    Automatically set to the current date and time when an object is first created.
    """

    updated_at = models.DateTimeField(auto_now=True)
    """
    Automatically set to the current date and time whenever an object is saved.
    """

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        """
        This class is marked as abstract, meaning it cannot be instantiated directly.
        Ordering is set to sort objects by created_at in descending order.
        """
