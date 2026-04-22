# notifications/views.py
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404


from .models import Notification
# Create your views here.

PAGE_SIZE = getattr(settings, "NOTIFICATIONS_PAGE_SIZE", 20)


@login_required
def list_notifications(request):
    qs = Notification.objects.filter(user=request.user)

    # optional filters
    f = request.GET.get("filter", "all")
    if f == "unread":
        qs = qs.filter(is_read=False)
    elif f == "read":
        qs = qs.filter(is_read=True)

    paginator = Paginator(qs, PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get("page"))
    ctx = {"page_obj": page_obj, "filter": f}
    return render(request, "notifications/list.html", ctx)


@login_required
def mark_read(request, pk):
    if request.method != "POST":
        raise Http404()

    # ✅ Using auto_id here instead of pk
    n = get_object_or_404(Notification, auto_id=pk, user=request.user)

    if not n.is_read:
        n.is_read = True
        n.save(update_fields=["is_read"])

    return JsonResponse({"ok": True})


@login_required
def mark_all_read(request):
    if request.method != "POST":
        raise Http404()

    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)

    return JsonResponse({"ok": True})


@login_required
def unread_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({"count": count})





