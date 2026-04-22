from django import forms
from django.contrib.auth import get_user_model


from .models import Measurements, DressType, Order, Fabric


class MeasurementsForm(forms.ModelForm):
    class Meta:
        model = Measurements
        exclude = ("customer", "auto_id", "created_at", "updated_at", "deleted_at",
            "is_active", "is_deleted", "created_by", "updated_by",
            "deleted_by", "language",)


    # def __init__(self, *args, **kwargs):
    #     dress_type = kwargs.pop("dress_type", None)
    #     super().__init__(*args, **kwargs)
    #
    #     # Hide all fields first
    #     for field in self.fields:
    #         self.fields[field].widget = forms.HiddenInput()
    #
    #     # Show only fields based on dress_type.required_fields
    #     if dress_type and dress_type.required_fields:
    #         for field_name in dress_type.required_fields:
    #             if field_name in self.fields:
    #                 self.fields[field_name].widget = forms.NumberInput(
    #                     attrs={"class": "form-control", "step": "0.1", "placeholder": f"Enter {field_name}"}
    #                 )
    #                 self.fields[field_name].label = field_name.capitalize()


    def __init__(self, *args, **kwargs):
        dress_type = kwargs.pop("dress_type", None)
        super().__init__(*args, **kwargs)
        self.fields['staff'].queryset = User.objects.filter(role=User.STAFF)



        if 'fabric' in self.fields:
            self.fields['fabric'].queryset = Fabric.objects.all()

        # If we're editing, get the dress_type from the instance
        if self.instance and self.instance.pk and not dress_type:
            dress_type = self.instance.dress_type



        # Initially make all measurement fields hidden or not required
        measurement_fields = [
            'height', 'weight', 'neck', 'shoulder', 'chest', 'bust', 'waist', 'hip',
            'back_length', 'front_length', 'torso', 'shoulder_to_bust', 'bust_span',
            'overbust', 'underbust', 'arm_length', 'half_sleeve', 'bicep', 'elbow',
            'wrist', 'armhole', 'shoulder_slope', 'neck_depth_front', 'neck_depth_back',
            'blouse_length', 'waist_to_hip', 'hip_depth', 'thigh', 'knee', 'calf',
            'ankle', 'crotch_depth', 'crotch_length_front', 'crotch_length_back',
            'inseam', 'outseam', 'pant_length', 'kurta_length', 'salwar_length',
            'churidar_length', 'lehenga_length', 'choli_length', 'gown_length',
            'anarkali_length', 'anarkali_flair', 'dupatta_length', 'shoulder_to_elbow',
            'waist_to_floor', 'armhole_depth', 'bust_separation', 'back_width', 'sleeve_length', 'stomach', 'skirt_length', 'length'
        ]

        for field_name in measurement_fields:
            if field_name in self.fields:
                self.fields[field_name].widget = forms.HiddenInput()
                self.fields[field_name].required = False

        always_visible_fields = ["dress_type", "fabric", "color"]

        for field_name in self.fields:
            if field_name not in always_visible_fields:
                self.fields[field_name].widget = forms.HiddenInput()
                self.fields[field_name].required = False

        # Explicitly set color as text input
        self.fields['color'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter color name (e.g., Red, Blue, etc.)'
        })
        self.fields['color'].required = True

        # Show only fields from DressType.required_fields
        if dress_type and dress_type.required_fields:
            for field_name in dress_type.required_fields:
                if field_name in self.fields:
                    self.fields[field_name].widget = forms.NumberInput(attrs={
                        "class": "form-control",
                        "step": "0.01",
                        "min": "0",
                        "placeholder": f"Enter {field_name.replace('_', ' ')} in cm"
                    })
                    self.fields[field_name].required = True
                    self.fields[field_name].label = field_name.replace('_', ' ').title()



class DressTypeForm(forms.ModelForm):
    class Meta:
        model = DressType
        fields = ["name", "description", "required_fields", "is_active"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "required_fields": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "placeholder": '["chest", "waist", "hip"]'}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


User = get_user_model()
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer", "order_date", "delivery_date", "status", "payment_status", "total_amount","no_of_items",
                  "notes"]

        widgets = {
            'color': forms.TextInput(attrs={
                'placeholder': "e.g., 'Royal Blue' or '#0000FF'",
                'class': 'form-control',
            }),
            'quantity': forms.NumberInput(attrs={
                'min': 1,
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fabric'].queryset = Fabric.objects.all()
        self.fields['fabric'].empty_label = "Select Fabric"
        self.fields['assigned_staff'].queryset = User.objects.filter(role=User.STAFF)
        self.fields['assigned_staff'].label = "Select Staff"
        self.fields['assigned_staff'].empty_label = "Choose a Staff Member"


