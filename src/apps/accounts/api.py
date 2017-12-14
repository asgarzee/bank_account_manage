from rest_framework import status, viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import BankAccount, Transaction
from .serializer import BankAccountSerializer, CreateAccountSerializer, CreateTransactionSerializer, \
    TransactionSerializer
from .utils import get_api_response


class BankAccountViewSet(viewsets.ModelViewSet):
    model = BankAccount
    serializer_class = BankAccountSerializer
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication, TokenAuthentication,
    )
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        serializer_action_classes = {
            'list': BankAccountSerializer,
            'retrieve': BankAccountSerializer,
            'create': CreateAccountSerializer
        }
        if hasattr(self, 'action'):
            return serializer_action_classes.get(self.action, self.serializer_class)
        return self.serializer_class

    def get_queryset(self):
        return self.model.objects.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        """
        Get list of all the accounts and its details
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response_data = get_api_response(data=response.data)
            return Response(response_data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        response_data = get_api_response(data=serializer.data)
        return Response(response_data)

    def retrieve(self, request, *args, **kwargs):
        """
        Get the details of a account
        """
        account_number = kwargs.get('account_number')
        try:
            account_object = self.model.objects.get(account_number=account_number)
        except self.model.DoesNotExist:
            response_data = get_api_response(message='Account does not exist', success=False)
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(account_object)
        response_data = get_api_response(data=serializer.data)
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Create a bank account

        Payload:
        ```
        {
          "balance": 10000,
          "last_name": "ned",
          "first_name": "stark"
        }
        ```
        Success Response:
        ```
        {
            "success": true,
            "message": "Successful",
            "data": {
                "account_number": "1513248658030792"
            }
        }
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_object = serializer.save(user=request.user)
        response_data = get_api_response(data={'account_number': account_object.account_number})
        return Response(response_data, status=status.HTTP_201_CREATED)


class TransactionViewSet(viewsets.ModelViewSet):
    model = Transaction
    serializer_class = TransactionSerializer
    authentication_classes = (
        JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication, TokenAuthentication
    )
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        serializer_action_classes = {
            'list': TransactionSerializer,
            'retrieve': TransactionSerializer,
            'create': CreateTransactionSerializer,
        }
        if hasattr(self, 'action'):
            return serializer_action_classes.get(self.action, self.serializer_class)
        return self.serializer_class

    def get_queryset(self):
        return self.model.objects.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        """
        Get list of all transactions
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response_data = get_api_response(data=response.data)
            return Response(response_data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        response_data = get_api_response(data=serializer.data)
        return Response(response_data)

    def retrieve(self, request, *args, **kwargs):
        """
        Get details of a transaction
        """
        reference_number = kwargs.get('reference_number')
        try:
            transaction_object = self.model.objects.get(reference_number=reference_number)
        except self.model.DoesNotExist:
            response_data = get_api_response(message='Transaction does not exist', success=False)
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(transaction_object)
        response_data = get_api_response(data=serializer.data)
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Debit, credit and transfer amount

        Payload for transfer:
        ```
        {
          "amount": 1000,
          "transaction_type": "transfer",
          "credit_account_number": "42492489234923",
          "debit_account_number": "87428378232389"
        }
        ```

        Payload for debit:
        ```
        {
          "amount": 1000,
          "transaction_type": "debit",
          "debit_account_number": "87428378232389"
        }
        ```

        Payload for credit:
        ```
        {
          "amount": 1000,
          "transaction_type": "credit",
          "credit_account_number": "42492489234923"
        }
        ```

        Success Response:
        ```
        {
          "message": "Successful",
          "data": {
            "amount": 1000,
            "reference_number": "1513249372422531",
            "modified_at": "2017-12-14T11:02:52.422928Z",
            "created_at": "2017-12-14T11:02:52.422877Z",
            "is_successful": true,
            "credit_account": "2343243243243",
            "debit_account": "1513240633758049"
          },
          "success": true
        }
        ```
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction_object, message = serializer.save(user=request.user)
        data = transaction_object.__dict__
        data.pop('_state', None)
        data.pop('id', None)
        response_data = get_api_response(data=data, message=message if message else 'Successful')
        return Response(response_data, status=status.HTTP_200_OK)
