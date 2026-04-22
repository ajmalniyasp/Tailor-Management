from django import forms

from orders.models import Measurements
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['order', 'rating', 'comments']
        widgets = {
            'order': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(FeedbackForm, self).__init__(*args, **kwargs)

        if self.user:
            # Filter measurements/orders that belong to the user
            # Exclude measurements that already have feedback
            available_orders = Measurements.objects.filter(
                customer=self.user
            ).exclude(
                feedback__isnull=False
            ).select_related('dress_type')

            # Create custom choices with better display
            choices = []
            for order in available_orders:
                display_text = self.get_order_display_text(order)
                choices.append((order.id, display_text))

            self.fields['order'].choices = [('', '---------')] + choices

    def get_order_display_text(self, order):
        """Generate a user-friendly display text for the order"""
        base_text = f"Order #{order.auto_id}"

        if order.dress_type:
            base_text += f" - {order.dress_type.name}"
        else:
            base_text += " - Custom Order"

        if order.color:
            base_text += f" - {order.color}"

        if order.date_added:
            base_text += f" - {order.date_added.strftime('%b %d, %Y')}"

        return base_text