from django.core.validators import MinValueValidator
from django.utils import timezone

from django.db import models
from django.conf import settings
from foundations.functions import get_auto_id
from foundations.models import BaseModel
from django.db.models import Max, Sum


class DressType(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    required_fields = models.JSONField(default=list)
    image = models.ImageField(upload_to='dress_types/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.auto_id:
            last = DressType.objects.all().order_by("auto_id").last()
            self.auto_id = last.auto_id + 1 if last else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "DressType"
        verbose_name_plural = "DressTypes"


class Measurements(BaseModel):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="measurements")
    dress_type = models.ForeignKey("DressType", on_delete=models.CASCADE, related_name="measurements", null=True,
                                   blank=True)
    measurements = models.JSONField(default=dict, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    staff = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True,limit_choices_to={'role': 3},
                              related_name="staff_measurements")

    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Height in cm")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Weight in kg")
    neck = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    shoulder = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    chest = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bust = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    waist = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hip = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    back_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    front_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    torso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    shoulder_to_bust = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bust_span = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    overbust = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    underbust = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    arm_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    half_sleeve = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bicep = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    elbow = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    wrist = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    armhole = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    shoulder_slope = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    neck_front = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    neck_back = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    blouse_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    waist_to_hip = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hip_depth = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    thigh = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    knee = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    calf = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ankle = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    crotch_depth = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    crotch_length_front = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    crotch_length_back = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    inseam = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    outseam = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pant_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    kurta_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    salwar_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    churidar_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    lehenga_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    choli_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    gown_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    anarkali_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    anarkali_flair = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dupatta_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    shoulder_to_elbow = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    waist_to_floor = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    armhole_depth = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bust_separation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    back_width = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sleeve_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    stomach = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    skirt_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    kameez_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    shirt_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bottom_waist = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bottom_width = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    bottom_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    jacket_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    shoulder_width = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cuff = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    high_hip = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    low_hip = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    rise = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    blouse_front_depth = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    blouse_back_depth = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    skirt_waist = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    Head_circumference = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    Neck_circumference = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    thobe_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    side_slit_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    abaya_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Show a more user-friendly representation
        if self.dress_type:
            return f"Order #{self.auto_id} - {self.dress_type.name} - {self.date_added.strftime('%b %d, %Y')}"
        else:
            return f"Order #{self.auto_id} - Custom Order - {self.date_added.strftime('%b %d, %Y')}"

    def get_measurements_list(self):
        """Return list of (field_name, value) for non-empty measurement fields"""
        measurements = []
        measurement_fields = [
            'height', 'weight', 'neck', 'shoulder', 'chest', 'bust', 'waist', 'hip',
            'back_length', 'front_length', 'torso', 'shoulder_to_bust', 'bust_span',
            'overbust', 'underbust', 'arm_length', 'half_sleeve', 'bicep', 'elbow',
            'wrist', 'armhole', 'shoulder_slope', 'neck_front', 'neck_back',
            'blouse_length', 'waist_to_hip', 'hip_depth', 'thigh', 'knee', 'calf',
            'ankle', 'crotch_depth', 'crotch_length_front', 'crotch_length_back',
            'inseam', 'outseam', 'pant_length', 'kurta_length', 'salwar_length',
            'churidar_length', 'lehenga_length', 'choli_length', 'gown_length',
            'anarkali_length', 'anarkali_flair', 'dupatta_length', 'shoulder_to_elbow',
            'waist_to_floor', 'armhole_depth', 'bust_separation', 'back_width', 'stomach', 'sleeve_length',
            'length', 'skirt_length', 'kameez_length', 'shirt_length', 'bottom_waist', 'bottom_width', 'bottom_length',
            'jacket_length', 'shoulder_width', 'cuff', 'high_hip', 'low_hip', 'rise', 'blouse_front_depth',
            'blouse_back_depth',
            'skirt_waist', 'Head_circumference', 'Neck_circumference', 'thobe_length', 'side_slit_length',
            'abaya_length'
        ]

        for field in measurement_fields:
            value = getattr(self, field)
            if value is not None and value != '':
                pretty = field.replace("_", " ").capitalize()
                measurements.append((field, float(value)))


        return measurements

    def get_measurements_json(self):
        """Return measurements as JSON for JavaScript"""
        measurements_dict = {}
        measurement_fields = [
            'height', 'weight', 'neck', 'shoulder', 'chest', 'bust', 'waist', 'hip',
            'back_length', 'front_length', 'torso', 'shoulder_to_bust', 'bust_span',
            'overbust', 'underbust', 'arm_length', 'half_sleeve', 'bicep', 'elbow',
            'wrist', 'armhole', 'shoulder_slope', 'neck_front', 'neck_back',
            'blouse_length', 'waist_to_hip', 'hip_depth', 'thigh', 'knee', 'calf',
            'ankle', 'crotch_depth', 'crotch_length_front', 'crotch_length_back',
            'inseam', 'outseam', 'pant_length', 'kurta_length', 'salwar_length',
            'churidar_length', 'lehenga_length', 'choli_length', 'gown_length',
            'anarkali_length', 'anarkali_flair', 'dupatta_length', 'shoulder_to_elbow',
            'waist_to_floor', 'armhole_depth', 'bust_separation', 'back_width', 'stomach', 'sleeve_length',
            'length', 'skirt_length', 'kameez_length', 'shirt_length', 'bottom_waist', 'bottom_width', 'bottom_length',
            'jacket_length', 'shoulder_width', 'cuff', 'high_hip', 'low_hip', 'rise', 'blouse_front_depth',
            'blouse_back_depth', 'skirt_waist', 'Head_circumference', 'Neck_circumference', 'thobe_length',
            'side_slit_length', 'abaya_length'
        ]

        for field in measurement_fields:
            value = getattr(self, field)
            if value is not None and value != '':
                measurements_dict[field] = float(value)

        return measurements_dict

    def save(self, *args, **kwargs):
        if not self.auto_id:
            # Get max auto_id for this table
            max_id = Measurements.objects.aggregate(Max('auto_id'))['auto_id__max'] or 0
            self.auto_id = max_id + 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Measurements"
        verbose_name_plural = "Measurements"

    def __str__(self):
        return f"{self.get_measurements_list()}"


class Fabric(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='fabric/', blank=True, null=True)

    def __str__(self):
        return self.name


class Order(BaseModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("unpaid", "Unpaid"),
        ("paid", "Paid"),
        ("refunded", "Refunded"),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="unpaid")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    no_of_items = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"

    def save(self, *args, **kwargs):
        if not self.auto_id:
            self.auto_id = get_auto_id(Order)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-order_date"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    measurement = models.ForeignKey(
        Measurements, on_delete=models.SET_NULL, null=True, blank=True, related_name="order_items"
    )

    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("cutting", "Cutting"),
        ("stitching", "Stitching"),
        ("ironing", "Ironing"),
        ("completed", "Completed"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_price(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        if not self.auto_id:
            self.auto_id = get_auto_id(self.__class__)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"(x{self.quantity})"

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
