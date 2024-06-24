# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tinkoff/invest/grpc/stoporders.proto
"""Generated protocol buffer code."""
from google.protobuf import (
    descriptor as _descriptor,
    descriptor_pool as _descriptor_pool,
    symbol_database as _symbol_database,
)
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2

from tinkoff.invest.grpc import (
    common_pb2 as tinkoff_dot_invest_dot_grpc_dot_common__pb2,
)
from tinkoff.invest.grpc.google.api import (
    field_behavior_pb2 as tinkoff_dot_invest_dot_grpc_dot_google_dot_api_dot_field__behavior__pb2,
)

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$tinkoff/invest/grpc/stoporders.proto\x12%tinkoff.public.invest.api.contract.v1\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x33tinkoff/invest/grpc/google/api/field_behavior.proto\x1a tinkoff/invest/grpc/common.proto\"\x97\n\n\x14PostStopOrderRequest\x12\x15\n\x04\x66igi\x18\x01 \x01(\tB\x02\x18\x01H\x00\x88\x01\x01\x12\x16\n\x08quantity\x18\x02 \x01(\x03\x42\x04\xe2\x41\x01\x02\x12\x44\n\x05price\x18\x03 \x01(\x0b\x32\x30.tinkoff.public.invest.api.contract.v1.QuotationH\x01\x88\x01\x01\x12I\n\nstop_price\x18\x04 \x01(\x0b\x32\x30.tinkoff.public.invest.api.contract.v1.QuotationH\x02\x88\x01\x01\x12R\n\tdirection\x18\x05 \x01(\x0e\x32\x39.tinkoff.public.invest.api.contract.v1.StopOrderDirectionB\x04\xe2\x41\x01\x02\x12\x18\n\naccount_id\x18\x06 \x01(\tB\x04\xe2\x41\x01\x02\x12]\n\x0f\x65xpiration_type\x18\x07 \x01(\x0e\x32>.tinkoff.public.invest.api.contract.v1.StopOrderExpirationTypeB\x04\xe2\x41\x01\x02\x12S\n\x0fstop_order_type\x18\x08 \x01(\x0e\x32\x34.tinkoff.public.invest.api.contract.v1.StopOrderTypeB\x04\xe2\x41\x01\x02\x12\x34\n\x0b\x65xpire_date\x18\t \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x03\x88\x01\x01\x12\x1b\n\rinstrument_id\x18\n \x01(\tB\x04\xe2\x41\x01\x02\x12U\n\x13\x65xchange_order_type\x18\x0b \x01(\x0e\x32\x38.tinkoff.public.invest.api.contract.v1.ExchangeOrderType\x12O\n\x10take_profit_type\x18\x0c \x01(\x0e\x32\x35.tinkoff.public.invest.api.contract.v1.TakeProfitType\x12_\n\rtrailing_data\x18\r \x01(\x0b\x32H.tinkoff.public.invest.api.contract.v1.PostStopOrderRequest.TrailingData\x12\x44\n\nprice_type\x18\x0e \x01(\x0e\x32\x30.tinkoff.public.invest.api.contract.v1.PriceType\x12\x16\n\x08order_id\x18\x0f \x01(\tB\x04\xe2\x41\x01\x02\x1a\xb0\x02\n\x0cTrailingData\x12@\n\x06indent\x18\x01 \x01(\x0b\x32\x30.tinkoff.public.invest.api.contract.v1.Quotation\x12M\n\x0bindent_type\x18\x02 \x01(\x0e\x32\x38.tinkoff.public.invest.api.contract.v1.TrailingValueType\x12@\n\x06spread\x18\x03 \x01(\x0b\x32\x30.tinkoff.public.invest.api.contract.v1.Quotation\x12M\n\x0bspread_type\x18\x04 \x01(\x0e\x32\x38.tinkoff.public.invest.api.contract.v1.TrailingValueTypeB\x07\n\x05_figiB\x08\n\x06_priceB\r\n\x0b_stop_priceB\x0e\n\x0c_expire_date\"\x9d\x01\n\x15PostStopOrderResponse\x12\x15\n\rstop_order_id\x18\x01 \x01(\t\x12\x18\n\x10order_request_id\x18\x02 \x01(\t\x12S\n\x11response_metadata\x18\xfe\x01 \x01(\x0b\x32\x37.tinkoff.public.invest.api.contract.v1.ResponseMetadata\"\xd0\x01\n\x14GetStopOrdersRequest\x12\x18\n\naccount_id\x18\x01 \x01(\tB\x04\xe2\x41\x01\x02\x12L\n\x06status\x18\x02 \x01(\x0e\x32<.tinkoff.public.invest.api.contract.v1.StopOrderStatusOption\x12(\n\x04\x66rom\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12&\n\x02to\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"^\n\x15GetStopOrdersResponse\x12\x45\n\x0bstop_orders\x18\x01 \x03(\x0b\x32\x30.tinkoff.public.invest.api.contract.v1.StopOrder\"O\n\x16\x43\x61ncelStopOrderRequest\x12\x18\n\naccount_id\x18\x01 \x01(\tB\x04\xe2\x41\x01\x02\x12\x1b\n\rstop_order_id\x18\x02 \x01(\tB\x04\xe2\x41\x01\x02\"C\n\x17\x43\x61ncelStopOrderResponse\x12(\n\x04time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\xfe\n\n\tStopOrder\x12\x15\n\rstop_order_id\x18\x01 \x01(\t\x12\x16\n\x0elots_requested\x18\x02 \x01(\x03\x12\x0c\n\x04\x66igi\x18\x03 \x01(\t\x12L\n\tdirection\x18\x04 \x01(\x0e\x32\x39.tinkoff.public.invest.api.contract.v1.StopOrderDirection\x12\x10\n\x08\x63urrency\x18\x05 \x01(\t\x12H\n\norder_type\x18\x06 \x01(\x0e\x32\x34.tinkoff.public.invest.api.contract.v1.StopOrderType\x12/\n\x0b\x63reate_date\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x38\n\x14\x61\x63tivation_date_time\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x33\n\x0f\x65xpiration_time\x18\t \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12@\n\x05price\x18\n \x01(\x0b\x32\x31.tinkoff.public.invest.api.contract.v1.MoneyValue\x12\x45\n\nstop_price\x18\x0b \x01(\x0b\x32\x31.tinkoff.public.invest.api.contract.v1.MoneyValue\x12\x16\n\x0einstrument_uid\x18\x0c \x01(\t\x12O\n\x10take_profit_type\x18\r \x01(\x0e\x32\x35.tinkoff.public.invest.api.contract.v1.TakeProfitType\x12T\n\rtrailing_data\x18\x0e \x01(\x0b\x32=.tinkoff.public.invest.api.contract.v1.StopOrder.TrailingData\x12L\n\x06status\x18\x0f \x01(\x0e\x32<.tinkoff.public.invest.api.contract.v1.StopOrderStatusOption\x12U\n\x13\x65xchange_order_type\x18\x10 \x01(\x0e\x32\x38.tinkoff.public.invest.api.contract.v1.ExchangeOrderType\x1a\xfc\x03\n\x0cTrailingData\x12@\n\x06indent\x18\x01 \x01(\x0b\x32\x30.tinkoff.public.invest.api.contract.v1.Quotation\x12M\n\x0bindent_type\x18\x02 \x01(\x0e\x32\x38.tinkoff.public.invest.api.contract.v1.TrailingValueType\x12@\n\x06spread\x18\x03 \x01(\x0b\x32\x30.tinkoff.public.invest.api.contract.v1.Quotation\x12M\n\x0bspread_type\x18\x04 \x01(\x0e\x32\x38.tinkoff.public.invest.api.contract.v1.TrailingValueType\x12I\n\x06status\x18\x05 \x01(\x0e\x32\x39.tinkoff.public.invest.api.contract.v1.TrailingStopStatus\x12?\n\x05price\x18\x07 \x01(\x0b\x32\x30.tinkoff.public.invest.api.contract.v1.Quotation\x12>\n\x04\x65xtr\x18\x08 \x01(\x0b\x32\x30.tinkoff.public.invest.api.contract.v1.Quotation*w\n\x12StopOrderDirection\x12$\n STOP_ORDER_DIRECTION_UNSPECIFIED\x10\x00\x12\x1c\n\x18STOP_ORDER_DIRECTION_BUY\x10\x01\x12\x1d\n\x19STOP_ORDER_DIRECTION_SELL\x10\x02*\xa5\x01\n\x17StopOrderExpirationType\x12*\n&STOP_ORDER_EXPIRATION_TYPE_UNSPECIFIED\x10\x00\x12/\n+STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_CANCEL\x10\x01\x12-\n)STOP_ORDER_EXPIRATION_TYPE_GOOD_TILL_DATE\x10\x02*\x90\x01\n\rStopOrderType\x12\x1f\n\x1bSTOP_ORDER_TYPE_UNSPECIFIED\x10\x00\x12\x1f\n\x1bSTOP_ORDER_TYPE_TAKE_PROFIT\x10\x01\x12\x1d\n\x19STOP_ORDER_TYPE_STOP_LOSS\x10\x02\x12\x1e\n\x1aSTOP_ORDER_TYPE_STOP_LIMIT\x10\x03*\xd2\x01\n\x15StopOrderStatusOption\x12!\n\x1dSTOP_ORDER_STATUS_UNSPECIFIED\x10\x00\x12\x19\n\x15STOP_ORDER_STATUS_ALL\x10\x01\x12\x1c\n\x18STOP_ORDER_STATUS_ACTIVE\x10\x02\x12\x1e\n\x1aSTOP_ORDER_STATUS_EXECUTED\x10\x03\x12\x1e\n\x1aSTOP_ORDER_STATUS_CANCELED\x10\x04\x12\x1d\n\x19STOP_ORDER_STATUS_EXPIRED\x10\x05*w\n\x11\x45xchangeOrderType\x12#\n\x1f\x45XCHANGE_ORDER_TYPE_UNSPECIFIED\x10\x00\x12\x1e\n\x1a\x45XCHANGE_ORDER_TYPE_MARKET\x10\x01\x12\x1d\n\x19\x45XCHANGE_ORDER_TYPE_LIMIT\x10\x02*o\n\x0eTakeProfitType\x12 \n\x1cTAKE_PROFIT_TYPE_UNSPECIFIED\x10\x00\x12\x1c\n\x18TAKE_PROFIT_TYPE_REGULAR\x10\x01\x12\x1d\n\x19TAKE_PROFIT_TYPE_TRAILING\x10\x02*m\n\x11TrailingValueType\x12\x1e\n\x1aTRAILING_VALUE_UNSPECIFIED\x10\x00\x12\x1b\n\x17TRAILING_VALUE_ABSOLUTE\x10\x01\x12\x1b\n\x17TRAILING_VALUE_RELATIVE\x10\x02*j\n\x12TrailingStopStatus\x12\x1d\n\x19TRAILING_STOP_UNSPECIFIED\x10\x00\x12\x18\n\x14TRAILING_STOP_ACTIVE\x10\x01\x12\x1b\n\x17TRAILING_STOP_ACTIVATED\x10\x02\x32\xc0\x03\n\x11StopOrdersService\x12\x8a\x01\n\rPostStopOrder\x12;.tinkoff.public.invest.api.contract.v1.PostStopOrderRequest\x1a<.tinkoff.public.invest.api.contract.v1.PostStopOrderResponse\x12\x8a\x01\n\rGetStopOrders\x12;.tinkoff.public.invest.api.contract.v1.GetStopOrdersRequest\x1a<.tinkoff.public.invest.api.contract.v1.GetStopOrdersResponse\x12\x90\x01\n\x0f\x43\x61ncelStopOrder\x12=.tinkoff.public.invest.api.contract.v1.CancelStopOrderRequest\x1a>.tinkoff.public.invest.api.contract.v1.CancelStopOrderResponseBa\n\x1cru.tinkoff.piapi.contract.v1P\x01Z\x0c./;investapi\xa2\x02\x05TIAPI\xaa\x02\x14Tinkoff.InvestApi.V1\xca\x02\x11Tinkoff\\Invest\\V1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tinkoff.invest.grpc.stoporders_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\034ru.tinkoff.piapi.contract.v1P\001Z\014./;investapi\242\002\005TIAPI\252\002\024Tinkoff.InvestApi.V1\312\002\021Tinkoff\\Invest\\V1'
  _POSTSTOPORDERREQUEST.fields_by_name['figi']._options = None
  _POSTSTOPORDERREQUEST.fields_by_name['figi']._serialized_options = b'\030\001'
  _POSTSTOPORDERREQUEST.fields_by_name['quantity']._options = None
  _POSTSTOPORDERREQUEST.fields_by_name['quantity']._serialized_options = b'\342A\001\002'
  _POSTSTOPORDERREQUEST.fields_by_name['direction']._options = None
  _POSTSTOPORDERREQUEST.fields_by_name['direction']._serialized_options = b'\342A\001\002'
  _POSTSTOPORDERREQUEST.fields_by_name['account_id']._options = None
  _POSTSTOPORDERREQUEST.fields_by_name['account_id']._serialized_options = b'\342A\001\002'
  _POSTSTOPORDERREQUEST.fields_by_name['expiration_type']._options = None
  _POSTSTOPORDERREQUEST.fields_by_name['expiration_type']._serialized_options = b'\342A\001\002'
  _POSTSTOPORDERREQUEST.fields_by_name['stop_order_type']._options = None
  _POSTSTOPORDERREQUEST.fields_by_name['stop_order_type']._serialized_options = b'\342A\001\002'
  _POSTSTOPORDERREQUEST.fields_by_name['instrument_id']._options = None
  _POSTSTOPORDERREQUEST.fields_by_name['instrument_id']._serialized_options = b'\342A\001\002'
  _POSTSTOPORDERREQUEST.fields_by_name['order_id']._options = None
  _POSTSTOPORDERREQUEST.fields_by_name['order_id']._serialized_options = b'\342A\001\002'
  _GETSTOPORDERSREQUEST.fields_by_name['account_id']._options = None
  _GETSTOPORDERSREQUEST.fields_by_name['account_id']._serialized_options = b'\342A\001\002'
  _CANCELSTOPORDERREQUEST.fields_by_name['account_id']._options = None
  _CANCELSTOPORDERREQUEST.fields_by_name['account_id']._serialized_options = b'\342A\001\002'
  _CANCELSTOPORDERREQUEST.fields_by_name['stop_order_id']._options = None
  _CANCELSTOPORDERREQUEST.fields_by_name['stop_order_id']._serialized_options = b'\342A\001\002'
  _globals['_STOPORDERDIRECTION']._serialized_start=3531
  _globals['_STOPORDERDIRECTION']._serialized_end=3650
  _globals['_STOPORDEREXPIRATIONTYPE']._serialized_start=3653
  _globals['_STOPORDEREXPIRATIONTYPE']._serialized_end=3818
  _globals['_STOPORDERTYPE']._serialized_start=3821
  _globals['_STOPORDERTYPE']._serialized_end=3965
  _globals['_STOPORDERSTATUSOPTION']._serialized_start=3968
  _globals['_STOPORDERSTATUSOPTION']._serialized_end=4178
  _globals['_EXCHANGEORDERTYPE']._serialized_start=4180
  _globals['_EXCHANGEORDERTYPE']._serialized_end=4299
  _globals['_TAKEPROFITTYPE']._serialized_start=4301
  _globals['_TAKEPROFITTYPE']._serialized_end=4412
  _globals['_TRAILINGVALUETYPE']._serialized_start=4414
  _globals['_TRAILINGVALUETYPE']._serialized_end=4523
  _globals['_TRAILINGSTOPSTATUS']._serialized_start=4525
  _globals['_TRAILINGSTOPSTATUS']._serialized_end=4631
  _globals['_POSTSTOPORDERREQUEST']._serialized_start=200
  _globals['_POSTSTOPORDERREQUEST']._serialized_end=1503
  _globals['_POSTSTOPORDERREQUEST_TRAILINGDATA']._serialized_start=1149
  _globals['_POSTSTOPORDERREQUEST_TRAILINGDATA']._serialized_end=1453
  _globals['_POSTSTOPORDERRESPONSE']._serialized_start=1506
  _globals['_POSTSTOPORDERRESPONSE']._serialized_end=1663
  _globals['_GETSTOPORDERSREQUEST']._serialized_start=1666
  _globals['_GETSTOPORDERSREQUEST']._serialized_end=1874
  _globals['_GETSTOPORDERSRESPONSE']._serialized_start=1876
  _globals['_GETSTOPORDERSRESPONSE']._serialized_end=1970
  _globals['_CANCELSTOPORDERREQUEST']._serialized_start=1972
  _globals['_CANCELSTOPORDERREQUEST']._serialized_end=2051
  _globals['_CANCELSTOPORDERRESPONSE']._serialized_start=2053
  _globals['_CANCELSTOPORDERRESPONSE']._serialized_end=2120
  _globals['_STOPORDER']._serialized_start=2123
  _globals['_STOPORDER']._serialized_end=3529
  _globals['_STOPORDER_TRAILINGDATA']._serialized_start=3021
  _globals['_STOPORDER_TRAILINGDATA']._serialized_end=3529
  _globals['_STOPORDERSSERVICE']._serialized_start=4634
  _globals['_STOPORDERSSERVICE']._serialized_end=5082
# @@protoc_insertion_point(module_scope)
