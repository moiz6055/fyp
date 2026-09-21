from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models


class User(AbstractUser):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Provider(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="provider"
    )

    cnic_number = models.CharField(max_length=15)
    cnic_image = models.ImageField(upload_to="cnic/")

    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)


    location = models.PointField(
        geography=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.name


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ProviderService(models.Model):
    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name="services"
    )

    service_category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name="providers"
    )



    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["provider", "service_category"],
                name="unique_provider_service"
            )
        ]

    def __str__(self):
        return f"{self.provider} - {self.service_category}"


class ServiceRequest(models.Model):

    STATUS_CHOICES = [
        ("SEARCHING", "Searching"),
        ("ACCEPTED", "Accepted"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="service_requests"
    )

    service = models.ForeignKey(
        ServiceCategory,
        on_delete=models.PROTECT,
        related_name="requests"
    )

    description = models.TextField()

    # Location where the client needs the service
    location = models.PointField(
        geography=True
    )

    assigned_provider = models.ForeignKey(
        Provider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_requests"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="SEARCHING"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request #{self.id}"