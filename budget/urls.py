from django.urls import path

from .views import BudgetView, ObjListView

app_name = "budget"


urlpatterns = [
    path("budget", BudgetView.as_view(), name="budget"),
    path("all_budgets", ObjListView.as_view(), name="get_budgets")
]