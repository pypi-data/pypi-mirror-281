# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gm/pb/fund_bnd_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='gm/pb/fund_bnd_service.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1cgm/pb/fund_bnd_service.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"`\n\x15GetConversionPriceReq\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x12\n\nstart_date\x18\x02 \x01(\t\x12\x10\n\x08\x65nd_date\x18\x03 \x01(\t\x12\x11\n\tdate_type\x18\x04 \x01(\t\"\xe3\x02\n\x0f\x43onversionPrice\x12,\n\x08pub_date\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x32\n\x0e\x65\x66\x66\x65\x63tive_date\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x32\n\x0e\x65xecution_date\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x18\n\x10\x63onversion_price\x18\x04 \x01(\x01\x12\x17\n\x0f\x63onversion_rate\x18\x05 \x01(\x01\x12\x19\n\x11\x63onversion_volume\x18\x06 \x01(\x01\x12\x1f\n\x17\x63onversion_amount_total\x18\x07 \x01(\x01\x12 \n\x18\x62ond_float_amount_remain\x18\x08 \x01(\x01\x12\x12\n\nevent_type\x18\t \x01(\t\x12\x15\n\rchange_reason\x18\n \x01(\t\"7\n\x15GetConversionPriceRsp\x12\x1e\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x10.ConversionPrice\"Y\n\x0eGetCallInfoReq\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x12\n\nstart_date\x18\x02 \x01(\t\x12\x10\n\x08\x65nd_date\x18\x03 \x01(\t\x12\x11\n\tdate_type\x18\x04 \x01(\t\"\x9e\x02\n\x08\x43\x61llInfo\x12,\n\x08pub_date\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12-\n\tcall_date\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0brecord_date\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12-\n\tcash_date\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x11\n\tcall_type\x18\x05 \x01(\t\x12\x13\n\x0b\x63\x61ll_reason\x18\x06 \x01(\t\x12\x12\n\ncall_price\x18\x07 \x01(\x01\x12\x19\n\x11interest_included\x18\t \x01(\x08\")\n\x0eGetCallInfoRsp\x12\x17\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\t.CallInfo\"X\n\rGetPutInfoReq\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x12\n\nstart_date\x18\x02 \x01(\t\x12\x10\n\x08\x65nd_date\x18\x03 \x01(\t\x12\x11\n\tdate_type\x18\x04 \x01(\t\"\x8e\x02\n\x07PutInfo\x12,\n\x08pub_date\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x32\n\x0eput_start_date\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x30\n\x0cput_end_date\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12-\n\tcash_date\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x12\n\nput_reason\x18\x05 \x01(\t\x12\x11\n\tput_price\x18\x06 \x01(\x01\x12\x19\n\x11interest_included\x18\x08 \x01(\x08\"\'\n\rGetPutInfoRsp\x12\x16\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x08.PutInfo\"r\n\x12GetAmountChangeReq\x12\x0e\n\x06symbol\x18\x01 \x01(\t\x12\x12\n\nstart_date\x18\x02 \x01(\t\x12\x10\n\x08\x65nd_date\x18\x03 \x01(\t\x12\x11\n\tdate_type\x18\x04 \x01(\t\x12\x13\n\x0b\x63hange_type\x18\x05 \x01(\x05\"\xb0\x01\n\x0c\x41mountChange\x12,\n\x08pub_date\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x13\n\x0b\x63hange_type\x18\x02 \x01(\t\x12/\n\x0b\x63hange_date\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x15\n\rchange_amount\x18\x04 \x01(\x01\x12\x15\n\rremain_amount\x18\x05 \x01(\x01\"1\n\x12GetAmountChangeRsp\x12\x1b\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\r.AmountChangeb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_GETCONVERSIONPRICEREQ = _descriptor.Descriptor(
  name='GetConversionPriceReq',
  full_name='GetConversionPriceReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='symbol', full_name='GetConversionPriceReq.symbol', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_date', full_name='GetConversionPriceReq.start_date', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end_date', full_name='GetConversionPriceReq.end_date', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='date_type', full_name='GetConversionPriceReq.date_type', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=65,
  serialized_end=161,
)


_CONVERSIONPRICE = _descriptor.Descriptor(
  name='ConversionPrice',
  full_name='ConversionPrice',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pub_date', full_name='ConversionPrice.pub_date', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='effective_date', full_name='ConversionPrice.effective_date', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='execution_date', full_name='ConversionPrice.execution_date', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='conversion_price', full_name='ConversionPrice.conversion_price', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='conversion_rate', full_name='ConversionPrice.conversion_rate', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='conversion_volume', full_name='ConversionPrice.conversion_volume', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='conversion_amount_total', full_name='ConversionPrice.conversion_amount_total', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bond_float_amount_remain', full_name='ConversionPrice.bond_float_amount_remain', index=7,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='event_type', full_name='ConversionPrice.event_type', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='change_reason', full_name='ConversionPrice.change_reason', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=164,
  serialized_end=519,
)


_GETCONVERSIONPRICERSP = _descriptor.Descriptor(
  name='GetConversionPriceRsp',
  full_name='GetConversionPriceRsp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='GetConversionPriceRsp.data', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=521,
  serialized_end=576,
)


_GETCALLINFOREQ = _descriptor.Descriptor(
  name='GetCallInfoReq',
  full_name='GetCallInfoReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='symbol', full_name='GetCallInfoReq.symbol', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_date', full_name='GetCallInfoReq.start_date', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end_date', full_name='GetCallInfoReq.end_date', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='date_type', full_name='GetCallInfoReq.date_type', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=578,
  serialized_end=667,
)


_CALLINFO = _descriptor.Descriptor(
  name='CallInfo',
  full_name='CallInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pub_date', full_name='CallInfo.pub_date', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='call_date', full_name='CallInfo.call_date', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='record_date', full_name='CallInfo.record_date', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cash_date', full_name='CallInfo.cash_date', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='call_type', full_name='CallInfo.call_type', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='call_reason', full_name='CallInfo.call_reason', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='call_price', full_name='CallInfo.call_price', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='interest_included', full_name='CallInfo.interest_included', index=7,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=670,
  serialized_end=956,
)


_GETCALLINFORSP = _descriptor.Descriptor(
  name='GetCallInfoRsp',
  full_name='GetCallInfoRsp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='GetCallInfoRsp.data', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=958,
  serialized_end=999,
)


_GETPUTINFOREQ = _descriptor.Descriptor(
  name='GetPutInfoReq',
  full_name='GetPutInfoReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='symbol', full_name='GetPutInfoReq.symbol', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_date', full_name='GetPutInfoReq.start_date', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end_date', full_name='GetPutInfoReq.end_date', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='date_type', full_name='GetPutInfoReq.date_type', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1001,
  serialized_end=1089,
)


_PUTINFO = _descriptor.Descriptor(
  name='PutInfo',
  full_name='PutInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pub_date', full_name='PutInfo.pub_date', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='put_start_date', full_name='PutInfo.put_start_date', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='put_end_date', full_name='PutInfo.put_end_date', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cash_date', full_name='PutInfo.cash_date', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='put_reason', full_name='PutInfo.put_reason', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='put_price', full_name='PutInfo.put_price', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='interest_included', full_name='PutInfo.interest_included', index=6,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1092,
  serialized_end=1362,
)


_GETPUTINFORSP = _descriptor.Descriptor(
  name='GetPutInfoRsp',
  full_name='GetPutInfoRsp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='GetPutInfoRsp.data', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1364,
  serialized_end=1403,
)


_GETAMOUNTCHANGEREQ = _descriptor.Descriptor(
  name='GetAmountChangeReq',
  full_name='GetAmountChangeReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='symbol', full_name='GetAmountChangeReq.symbol', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='start_date', full_name='GetAmountChangeReq.start_date', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='end_date', full_name='GetAmountChangeReq.end_date', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='date_type', full_name='GetAmountChangeReq.date_type', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='change_type', full_name='GetAmountChangeReq.change_type', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1405,
  serialized_end=1519,
)


_AMOUNTCHANGE = _descriptor.Descriptor(
  name='AmountChange',
  full_name='AmountChange',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pub_date', full_name='AmountChange.pub_date', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='change_type', full_name='AmountChange.change_type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='change_date', full_name='AmountChange.change_date', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='change_amount', full_name='AmountChange.change_amount', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='remain_amount', full_name='AmountChange.remain_amount', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1522,
  serialized_end=1698,
)


_GETAMOUNTCHANGERSP = _descriptor.Descriptor(
  name='GetAmountChangeRsp',
  full_name='GetAmountChangeRsp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='GetAmountChangeRsp.data', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1700,
  serialized_end=1749,
)

_CONVERSIONPRICE.fields_by_name['pub_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_CONVERSIONPRICE.fields_by_name['effective_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_CONVERSIONPRICE.fields_by_name['execution_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_GETCONVERSIONPRICERSP.fields_by_name['data'].message_type = _CONVERSIONPRICE
_CALLINFO.fields_by_name['pub_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_CALLINFO.fields_by_name['call_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_CALLINFO.fields_by_name['record_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_CALLINFO.fields_by_name['cash_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_GETCALLINFORSP.fields_by_name['data'].message_type = _CALLINFO
_PUTINFO.fields_by_name['pub_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_PUTINFO.fields_by_name['put_start_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_PUTINFO.fields_by_name['put_end_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_PUTINFO.fields_by_name['cash_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_GETPUTINFORSP.fields_by_name['data'].message_type = _PUTINFO
_AMOUNTCHANGE.fields_by_name['pub_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_AMOUNTCHANGE.fields_by_name['change_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_GETAMOUNTCHANGERSP.fields_by_name['data'].message_type = _AMOUNTCHANGE
DESCRIPTOR.message_types_by_name['GetConversionPriceReq'] = _GETCONVERSIONPRICEREQ
DESCRIPTOR.message_types_by_name['ConversionPrice'] = _CONVERSIONPRICE
DESCRIPTOR.message_types_by_name['GetConversionPriceRsp'] = _GETCONVERSIONPRICERSP
DESCRIPTOR.message_types_by_name['GetCallInfoReq'] = _GETCALLINFOREQ
DESCRIPTOR.message_types_by_name['CallInfo'] = _CALLINFO
DESCRIPTOR.message_types_by_name['GetCallInfoRsp'] = _GETCALLINFORSP
DESCRIPTOR.message_types_by_name['GetPutInfoReq'] = _GETPUTINFOREQ
DESCRIPTOR.message_types_by_name['PutInfo'] = _PUTINFO
DESCRIPTOR.message_types_by_name['GetPutInfoRsp'] = _GETPUTINFORSP
DESCRIPTOR.message_types_by_name['GetAmountChangeReq'] = _GETAMOUNTCHANGEREQ
DESCRIPTOR.message_types_by_name['AmountChange'] = _AMOUNTCHANGE
DESCRIPTOR.message_types_by_name['GetAmountChangeRsp'] = _GETAMOUNTCHANGERSP
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetConversionPriceReq = _reflection.GeneratedProtocolMessageType('GetConversionPriceReq', (_message.Message,), {
  'DESCRIPTOR' : _GETCONVERSIONPRICEREQ,
  '__module__' : 'gm.pb.fund_bnd_service_pb2'
  # @@protoc_insertion_point(class_scope:GetConversionPriceReq)
  })
_sym_db.RegisterMessage(GetConversionPriceReq)

ConversionPrice = _reflection.GeneratedProtocolMessageType('ConversionPrice', (_message.Message,), {
  'DESCRIPTOR' : _CONVERSIONPRICE,
  '__module__' : 'gm.pb.fund_bnd_service_pb2'
  # @@protoc_insertion_point(class_scope:ConversionPrice)
  })
_sym_db.RegisterMessage(ConversionPrice)

GetConversionPriceRsp = _reflection.GeneratedProtocolMessageType('GetConversionPriceRsp', (_message.Message,), {
  'DESCRIPTOR' : _GETCONVERSIONPRICERSP,
  '__module__' : 'gm.pb.fund_bnd_service_pb2'
  # @@protoc_insertion_point(class_scope:GetConversionPriceRsp)
  })
_sym_db.RegisterMessage(GetConversionPriceRsp)

GetCallInfoReq = _reflection.GeneratedProtocolMessageType('GetCallInfoReq', (_message.Message,), {
  'DESCRIPTOR' : _GETCALLINFOREQ,
  '__module__' : 'gm.pb.fund_bnd_service_pb2'
  # @@protoc_insertion_point(class_scope:GetCallInfoReq)
  })
_sym_db.RegisterMessage(GetCallInfoReq)

CallInfo = _reflection.GeneratedProtocolMessageType('CallInfo', (_message.Message,), {
  'DESCRIPTOR' : _CALLINFO,
  '__module__' : 'gm.pb.fund_bnd_service_pb2'
  # @@protoc_insertion_point(class_scope:CallInfo)
  })
_sym_db.RegisterMessage(CallInfo)

GetCallInfoRsp = _reflection.GeneratedProtocolMessageType('GetCallInfoRsp', (_message.Message,), {
  'DESCRIPTOR' : _GETCALLINFORSP,
  '__module__' : 'gm.pb.fund_bnd_service_pb2'
  # @@protoc_insertion_point(class_scope:GetCallInfoRsp)
  })
_sym_db.RegisterMessage(GetCallInfoRsp)

GetPutInfoReq = _reflection.GeneratedProtocolMessageType('GetPutInfoReq', (_message.Message,), {
  'DESCRIPTOR' : _GETPUTINFOREQ,
  '__module__' : 'gm.pb.fund_bnd_service_pb2'
  # @@protoc_insertion_point(class_scope:GetPutInfoReq)
  })
_sym_db.RegisterMessage(GetPutInfoReq)

PutInfo = _reflection.GeneratedProtocolMessageType('PutInfo', (_message.Message,), {
  'DESCRIPTOR' : _PUTINFO,
  '__module__' : 'gm.pb.fund_bnd_service_pb2'
  # @@protoc_insertion_point(class_scope:PutInfo)
  })
_sym_db.RegisterMessage(PutInfo)

GetPutInfoRsp = _reflection.GeneratedProtocolMessageType('GetPutInfoRsp', (_message.Message,), {
  'DESCRIPTOR' : _GETPUTINFORSP,
  '__module__' : 'gm.pb.fund_bnd_service_pb2'
  # @@protoc_insertion_point(class_scope:GetPutInfoRsp)
  })
_sym_db.RegisterMessage(GetPutInfoRsp)

GetAmountChangeReq = _reflection.GeneratedProtocolMessageType('GetAmountChangeReq', (_message.Message,), {
  'DESCRIPTOR' : _GETAMOUNTCHANGEREQ,
  '__module__' : 'gm.pb.fund_bnd_service_pb2'
  # @@protoc_insertion_point(class_scope:GetAmountChangeReq)
  })
_sym_db.RegisterMessage(GetAmountChangeReq)

AmountChange = _reflection.GeneratedProtocolMessageType('AmountChange', (_message.Message,), {
  'DESCRIPTOR' : _AMOUNTCHANGE,
  '__module__' : 'gm.pb.fund_bnd_service_pb2'
  # @@protoc_insertion_point(class_scope:AmountChange)
  })
_sym_db.RegisterMessage(AmountChange)

GetAmountChangeRsp = _reflection.GeneratedProtocolMessageType('GetAmountChangeRsp', (_message.Message,), {
  'DESCRIPTOR' : _GETAMOUNTCHANGERSP,
  '__module__' : 'gm.pb.fund_bnd_service_pb2'
  # @@protoc_insertion_point(class_scope:GetAmountChangeRsp)
  })
_sym_db.RegisterMessage(GetAmountChangeRsp)


# @@protoc_insertion_point(module_scope)
