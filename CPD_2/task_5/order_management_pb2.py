# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: order_management.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16order_management.proto\x12\tecommerce\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1bgoogle/protobuf/empty.proto\"[\n\x05Order\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05items\x18\x02 \x03(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\r\n\x05price\x18\x04 \x01(\x02\x12\x13\n\x0b\x64\x65stination\x18\x05 \x01(\t\"T\n\x10\x43ombinedShipment\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\x12$\n\nordersList\x18\x03 \x03(\x0b\x32\x10.ecommerce.Order2\xa2\x03\n\x0fOrderManagement\x12:\n\x08\x61\x64\x64Order\x12\x10.ecommerce.Order\x1a\x1c.google.protobuf.StringValue\x12:\n\x08getOrder\x12\x1c.google.protobuf.StringValue\x1a\x10.ecommerce.Order\x12@\n\x0csearchOrders\x12\x1c.google.protobuf.StringValue\x1a\x10.ecommerce.Order0\x01\x12@\n\x0cupdateOrders\x12\x10.ecommerce.Order\x1a\x1c.google.protobuf.StringValue(\x01\x12N\n\rprocessOrders\x12\x1c.google.protobuf.StringValue\x1a\x1b.ecommerce.CombinedShipment(\x01\x30\x01\x12\x43\n\x0b\x64\x65leteOrder\x12\x1c.google.protobuf.StringValue\x1a\x16.google.protobuf.Emptyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_management_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ORDER']._serialized_start=98
  _globals['_ORDER']._serialized_end=189
  _globals['_COMBINEDSHIPMENT']._serialized_start=191
  _globals['_COMBINEDSHIPMENT']._serialized_end=275
  _globals['_ORDERMANAGEMENT']._serialized_start=278
  _globals['_ORDERMANAGEMENT']._serialized_end=696
# @@protoc_insertion_point(module_scope)
