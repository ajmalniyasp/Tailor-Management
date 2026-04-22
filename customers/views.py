from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from foundations.functions import get_auto_id
from .models import Feedback
from .forms import FeedbackForm
from orders.models import Measurements
from django.contrib import messages


@login_required
def submit_feedback(request, order_id=None):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                feedback = form.save(commit=False)
                feedback.customer = request.user
                feedback.created_by = request.user
                feedback.auto_id = get_auto_id(Feedback)
                feedback.save()

                # Debug print
                print(
                    f"✅ Feedback saved successfully! ID: {feedback.id}, Customer: {request.user}, Order: {feedback.order.id}")
                messages.success(request, "Thank you for your feedback!")
                return redirect('customers:thank_you')

            except Exception as e:
                # Debug print
                print(f"❌ Error saving feedback: {str(e)}")
                return render(request, 'customers/feedback/submit_feedback.html', {
                    'form': form,
                    'error': f'An error occurred while saving your feedback: {str(e)}'
                })
        else:
            # Debug print for form errors
            print(f"❌ Form errors: {form.errors}")
    else:
        # If order_id is provided, pre-select that order
        initial = {}
        if order_id:
            try:
                order = Measurements.objects.get(
                    id=order_id,
                    customer=request.user
                )
                # Check if feedback already exists
                if not Feedback.objects.filter(customer=request.user, order=order).exists():
                    initial['order'] = order
                else:
                    messages.warning(request, "You have already submitted feedback for this order.")
            except Measurements.DoesNotExist:
                messages.error(request, "Order not found.")

        form = FeedbackForm(initial=initial, user=request.user)

    # Get available orders for the template context
    available_orders = Measurements.objects.filter(
        customer=request.user
    ).exclude(
        feedback__isnull=False
    ).select_related('dress_type')

    return render(request, 'customers/feedback/submit_feedback.html', {
        'form': form,
        'available_orders': available_orders,
        'order_id': order_id
    })


@login_required
def feedback_list(request):
    # For customers, show only their feedback
    # For staff, show all feedback
    if request.user.is_staff:
        feedback_list = Feedback.objects.all().select_related(
            'customer', 'order', 'order__dress_type'
        ).order_by('-created_at')
    else:
        feedback_list = Feedback.objects.filter(customer=request.user).select_related(
            'order', 'order__dress_type'
        ).order_by('-created_at')

    paginator = Paginator(feedback_list, 10)  # Show 10 feedback per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'feedback_count': feedback_list.count()
    }
    return render(request, 'customers/feedback/view_feedbacks.html', context)


def thank_you(request):
    return render(request, 'customers/feedback/thank_you.html')