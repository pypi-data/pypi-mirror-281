# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from tinkoff.invest.grpc import (
    operations_pb2 as tinkoff_dot_invest_dot_grpc_dot_operations__pb2,
    orders_pb2 as tinkoff_dot_invest_dot_grpc_dot_orders__pb2,
    sandbox_pb2 as tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2,
    users_pb2 as tinkoff_dot_invest_dot_grpc_dot_users__pb2,
)


class SandboxServiceStub(object):
    """Методы для работы с песочницей Tinkoff Invest API
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.OpenSandboxAccount = channel.unary_unary(
                '/tinkoff.public.invest.api.contract.v1.SandboxService/OpenSandboxAccount',
                request_serializer=tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2.OpenSandboxAccountRequest.SerializeToString,
                response_deserializer=tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2.OpenSandboxAccountResponse.FromString,
                )
        self.GetSandboxAccounts = channel.unary_unary(
                '/tinkoff.public.invest.api.contract.v1.SandboxService/GetSandboxAccounts',
                request_serializer=tinkoff_dot_invest_dot_grpc_dot_users__pb2.GetAccountsRequest.SerializeToString,
                response_deserializer=tinkoff_dot_invest_dot_grpc_dot_users__pb2.GetAccountsResponse.FromString,
                )
        self.CloseSandboxAccount = channel.unary_unary(
                '/tinkoff.public.invest.api.contract.v1.SandboxService/CloseSandboxAccount',
                request_serializer=tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2.CloseSandboxAccountRequest.SerializeToString,
                response_deserializer=tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2.CloseSandboxAccountResponse.FromString,
                )
        self.PostSandboxOrder = channel.unary_unary(
                '/tinkoff.public.invest.api.contract.v1.SandboxService/PostSandboxOrder',
                request_serializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.PostOrderRequest.SerializeToString,
                response_deserializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.PostOrderResponse.FromString,
                )
        self.ReplaceSandboxOrder = channel.unary_unary(
                '/tinkoff.public.invest.api.contract.v1.SandboxService/ReplaceSandboxOrder',
                request_serializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.ReplaceOrderRequest.SerializeToString,
                response_deserializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.PostOrderResponse.FromString,
                )
        self.GetSandboxOrders = channel.unary_unary(
                '/tinkoff.public.invest.api.contract.v1.SandboxService/GetSandboxOrders',
                request_serializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.GetOrdersRequest.SerializeToString,
                response_deserializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.GetOrdersResponse.FromString,
                )
        self.CancelSandboxOrder = channel.unary_unary(
                '/tinkoff.public.invest.api.contract.v1.SandboxService/CancelSandboxOrder',
                request_serializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.CancelOrderRequest.SerializeToString,
                response_deserializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.CancelOrderResponse.FromString,
                )
        self.GetSandboxOrderState = channel.unary_unary(
                '/tinkoff.public.invest.api.contract.v1.SandboxService/GetSandboxOrderState',
                request_serializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.GetOrderStateRequest.SerializeToString,
                response_deserializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.OrderState.FromString,
                )
        self.GetSandboxPositions = channel.unary_unary(
                '/tinkoff.public.invest.api.contract.v1.SandboxService/GetSandboxPositions',
                request_serializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.PositionsRequest.SerializeToString,
                response_deserializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.PositionsResponse.FromString,
                )
        self.GetSandboxOperations = channel.unary_unary(
                '/tinkoff.public.invest.api.contract.v1.SandboxService/GetSandboxOperations',
                request_serializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.OperationsRequest.SerializeToString,
                response_deserializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.OperationsResponse.FromString,
                )
        self.GetSandboxOperationsByCursor = channel.unary_unary(
                '/tinkoff.public.invest.api.contract.v1.SandboxService/GetSandboxOperationsByCursor',
                request_serializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.GetOperationsByCursorRequest.SerializeToString,
                response_deserializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.GetOperationsByCursorResponse.FromString,
                )
        self.GetSandboxPortfolio = channel.unary_unary(
                '/tinkoff.public.invest.api.contract.v1.SandboxService/GetSandboxPortfolio',
                request_serializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.PortfolioRequest.SerializeToString,
                response_deserializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.PortfolioResponse.FromString,
                )
        self.SandboxPayIn = channel.unary_unary(
                '/tinkoff.public.invest.api.contract.v1.SandboxService/SandboxPayIn',
                request_serializer=tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2.SandboxPayInRequest.SerializeToString,
                response_deserializer=tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2.SandboxPayInResponse.FromString,
                )
        self.GetSandboxWithdrawLimits = channel.unary_unary(
                '/tinkoff.public.invest.api.contract.v1.SandboxService/GetSandboxWithdrawLimits',
                request_serializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.WithdrawLimitsRequest.SerializeToString,
                response_deserializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.WithdrawLimitsResponse.FromString,
                )
        self.GetSandboxMaxLots = channel.unary_unary(
                '/tinkoff.public.invest.api.contract.v1.SandboxService/GetSandboxMaxLots',
                request_serializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.GetMaxLotsRequest.SerializeToString,
                response_deserializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.GetMaxLotsResponse.FromString,
                )


class SandboxServiceServicer(object):
    """Методы для работы с песочницей Tinkoff Invest API
    """

    def OpenSandboxAccount(self, request, context):
        """Зарегистрировать счёт.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSandboxAccounts(self, request, context):
        """Получить счета.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CloseSandboxAccount(self, request, context):
        """Закрыть счёт.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PostSandboxOrder(self, request, context):
        """Выставить торговое поручение.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReplaceSandboxOrder(self, request, context):
        """Изменить выставленную заявку.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSandboxOrders(self, request, context):
        """Получить список активных заявок по счёту.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelSandboxOrder(self, request, context):
        """Отменить торговое поручение.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSandboxOrderState(self, request, context):
        """Поулчить статус заявки в песочнице. Заявки хранятся в таблице 7 дней.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSandboxPositions(self, request, context):
        """Получить позиции по виртуальному счёту.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSandboxOperations(self, request, context):
        """Получить операции по номеру счёта.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSandboxOperationsByCursor(self, request, context):
        """Получить операции по номеру счёта с пагинацией.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSandboxPortfolio(self, request, context):
        """Получить портфель.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SandboxPayIn(self, request, context):
        """Пополнить счёт.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSandboxWithdrawLimits(self, request, context):
        """Получить доступный остаток для вывода средств.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSandboxMaxLots(self, request, context):
        """Расчёт количества доступных для покупки/продажи лотов в песочнице.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SandboxServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'OpenSandboxAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.OpenSandboxAccount,
                    request_deserializer=tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2.OpenSandboxAccountRequest.FromString,
                    response_serializer=tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2.OpenSandboxAccountResponse.SerializeToString,
            ),
            'GetSandboxAccounts': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSandboxAccounts,
                    request_deserializer=tinkoff_dot_invest_dot_grpc_dot_users__pb2.GetAccountsRequest.FromString,
                    response_serializer=tinkoff_dot_invest_dot_grpc_dot_users__pb2.GetAccountsResponse.SerializeToString,
            ),
            'CloseSandboxAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.CloseSandboxAccount,
                    request_deserializer=tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2.CloseSandboxAccountRequest.FromString,
                    response_serializer=tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2.CloseSandboxAccountResponse.SerializeToString,
            ),
            'PostSandboxOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.PostSandboxOrder,
                    request_deserializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.PostOrderRequest.FromString,
                    response_serializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.PostOrderResponse.SerializeToString,
            ),
            'ReplaceSandboxOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.ReplaceSandboxOrder,
                    request_deserializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.ReplaceOrderRequest.FromString,
                    response_serializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.PostOrderResponse.SerializeToString,
            ),
            'GetSandboxOrders': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSandboxOrders,
                    request_deserializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.GetOrdersRequest.FromString,
                    response_serializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.GetOrdersResponse.SerializeToString,
            ),
            'CancelSandboxOrder': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelSandboxOrder,
                    request_deserializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.CancelOrderRequest.FromString,
                    response_serializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.CancelOrderResponse.SerializeToString,
            ),
            'GetSandboxOrderState': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSandboxOrderState,
                    request_deserializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.GetOrderStateRequest.FromString,
                    response_serializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.OrderState.SerializeToString,
            ),
            'GetSandboxPositions': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSandboxPositions,
                    request_deserializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.PositionsRequest.FromString,
                    response_serializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.PositionsResponse.SerializeToString,
            ),
            'GetSandboxOperations': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSandboxOperations,
                    request_deserializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.OperationsRequest.FromString,
                    response_serializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.OperationsResponse.SerializeToString,
            ),
            'GetSandboxOperationsByCursor': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSandboxOperationsByCursor,
                    request_deserializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.GetOperationsByCursorRequest.FromString,
                    response_serializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.GetOperationsByCursorResponse.SerializeToString,
            ),
            'GetSandboxPortfolio': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSandboxPortfolio,
                    request_deserializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.PortfolioRequest.FromString,
                    response_serializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.PortfolioResponse.SerializeToString,
            ),
            'SandboxPayIn': grpc.unary_unary_rpc_method_handler(
                    servicer.SandboxPayIn,
                    request_deserializer=tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2.SandboxPayInRequest.FromString,
                    response_serializer=tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2.SandboxPayInResponse.SerializeToString,
            ),
            'GetSandboxWithdrawLimits': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSandboxWithdrawLimits,
                    request_deserializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.WithdrawLimitsRequest.FromString,
                    response_serializer=tinkoff_dot_invest_dot_grpc_dot_operations__pb2.WithdrawLimitsResponse.SerializeToString,
            ),
            'GetSandboxMaxLots': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSandboxMaxLots,
                    request_deserializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.GetMaxLotsRequest.FromString,
                    response_serializer=tinkoff_dot_invest_dot_grpc_dot_orders__pb2.GetMaxLotsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tinkoff.public.invest.api.contract.v1.SandboxService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SandboxService(object):
    """Методы для работы с песочницей Tinkoff Invest API
    """

    @staticmethod
    def OpenSandboxAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tinkoff.public.invest.api.contract.v1.SandboxService/OpenSandboxAccount',
            tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2.OpenSandboxAccountRequest.SerializeToString,
            tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2.OpenSandboxAccountResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSandboxAccounts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tinkoff.public.invest.api.contract.v1.SandboxService/GetSandboxAccounts',
            tinkoff_dot_invest_dot_grpc_dot_users__pb2.GetAccountsRequest.SerializeToString,
            tinkoff_dot_invest_dot_grpc_dot_users__pb2.GetAccountsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CloseSandboxAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tinkoff.public.invest.api.contract.v1.SandboxService/CloseSandboxAccount',
            tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2.CloseSandboxAccountRequest.SerializeToString,
            tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2.CloseSandboxAccountResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PostSandboxOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tinkoff.public.invest.api.contract.v1.SandboxService/PostSandboxOrder',
            tinkoff_dot_invest_dot_grpc_dot_orders__pb2.PostOrderRequest.SerializeToString,
            tinkoff_dot_invest_dot_grpc_dot_orders__pb2.PostOrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReplaceSandboxOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tinkoff.public.invest.api.contract.v1.SandboxService/ReplaceSandboxOrder',
            tinkoff_dot_invest_dot_grpc_dot_orders__pb2.ReplaceOrderRequest.SerializeToString,
            tinkoff_dot_invest_dot_grpc_dot_orders__pb2.PostOrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSandboxOrders(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tinkoff.public.invest.api.contract.v1.SandboxService/GetSandboxOrders',
            tinkoff_dot_invest_dot_grpc_dot_orders__pb2.GetOrdersRequest.SerializeToString,
            tinkoff_dot_invest_dot_grpc_dot_orders__pb2.GetOrdersResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CancelSandboxOrder(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tinkoff.public.invest.api.contract.v1.SandboxService/CancelSandboxOrder',
            tinkoff_dot_invest_dot_grpc_dot_orders__pb2.CancelOrderRequest.SerializeToString,
            tinkoff_dot_invest_dot_grpc_dot_orders__pb2.CancelOrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSandboxOrderState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tinkoff.public.invest.api.contract.v1.SandboxService/GetSandboxOrderState',
            tinkoff_dot_invest_dot_grpc_dot_orders__pb2.GetOrderStateRequest.SerializeToString,
            tinkoff_dot_invest_dot_grpc_dot_orders__pb2.OrderState.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSandboxPositions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tinkoff.public.invest.api.contract.v1.SandboxService/GetSandboxPositions',
            tinkoff_dot_invest_dot_grpc_dot_operations__pb2.PositionsRequest.SerializeToString,
            tinkoff_dot_invest_dot_grpc_dot_operations__pb2.PositionsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSandboxOperations(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tinkoff.public.invest.api.contract.v1.SandboxService/GetSandboxOperations',
            tinkoff_dot_invest_dot_grpc_dot_operations__pb2.OperationsRequest.SerializeToString,
            tinkoff_dot_invest_dot_grpc_dot_operations__pb2.OperationsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSandboxOperationsByCursor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tinkoff.public.invest.api.contract.v1.SandboxService/GetSandboxOperationsByCursor',
            tinkoff_dot_invest_dot_grpc_dot_operations__pb2.GetOperationsByCursorRequest.SerializeToString,
            tinkoff_dot_invest_dot_grpc_dot_operations__pb2.GetOperationsByCursorResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSandboxPortfolio(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tinkoff.public.invest.api.contract.v1.SandboxService/GetSandboxPortfolio',
            tinkoff_dot_invest_dot_grpc_dot_operations__pb2.PortfolioRequest.SerializeToString,
            tinkoff_dot_invest_dot_grpc_dot_operations__pb2.PortfolioResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SandboxPayIn(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tinkoff.public.invest.api.contract.v1.SandboxService/SandboxPayIn',
            tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2.SandboxPayInRequest.SerializeToString,
            tinkoff_dot_invest_dot_grpc_dot_sandbox__pb2.SandboxPayInResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSandboxWithdrawLimits(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tinkoff.public.invest.api.contract.v1.SandboxService/GetSandboxWithdrawLimits',
            tinkoff_dot_invest_dot_grpc_dot_operations__pb2.WithdrawLimitsRequest.SerializeToString,
            tinkoff_dot_invest_dot_grpc_dot_operations__pb2.WithdrawLimitsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSandboxMaxLots(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tinkoff.public.invest.api.contract.v1.SandboxService/GetSandboxMaxLots',
            tinkoff_dot_invest_dot_grpc_dot_orders__pb2.GetMaxLotsRequest.SerializeToString,
            tinkoff_dot_invest_dot_grpc_dot_orders__pb2.GetMaxLotsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
