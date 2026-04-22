from django.db.models import Sum, F


def update_order_totals(order):
    """
    Recalculate and update total amount and item count for an order.
    """
    aggregates = order.items.aggregate(
        total=Sum(F("price") * F("quantity")),
        count=Sum("quantity")
    )

    order.total_amount = aggregates["total"] or 0
    order.no_of_items = order.items.count()
    order.save(update_fields=["total_amount", "no_of_items"])