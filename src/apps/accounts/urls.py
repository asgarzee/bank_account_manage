from django.conf.urls import url

from .api import BankAccountViewSet, TransactionViewSet

urlpatterns = [
    url(r'^accounts/$', BankAccountViewSet.as_view({'get': 'list', 'post': 'create'}), name="accounts_list_and_create"),
    url(r'^accounts/(?P<account_number>\w+)/$', BankAccountViewSet.as_view({'get': 'retrieve'}),
        name="accounts_retrieve"),
    url(r'^transactions/$', TransactionViewSet.as_view({'get': 'list'}), name="transactions_list"),
    url(r'^transactions/(?P<reference_number>\w+)/$', TransactionViewSet.as_view({'get': 'retrieve'}),
        name="transactions_retrieve"),
    url(r'^transfers/$', TransactionViewSet.as_view({'post': 'create'}), name="transactions_create"),

]
