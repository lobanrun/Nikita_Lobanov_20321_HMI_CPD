# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: product_info.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12product_info.proto\x12\tecommerce\x1a\x1bgoogle/protobuf/empty.proto\"G\n\x07Product\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\r\n\x05price\x18\x04 \x01(\x02\"\x1a\n\tProductID\x12\r\n\x05value\x18\x01 \x01(\t2\xbc\x01\n\x0bProductInfo\x12\x36\n\naddProduct\x12\x12.ecommerce.Product\x1a\x14.ecommerce.ProductID\x12\x36\n\ngetProduct\x12\x14.ecommerce.ProductID\x1a\x12.ecommerce.Product\x12=\n\rdeleteProduct\x12\x14.ecommerce.ProductID\x1a\x16.google.protobuf.Emptyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'product_info_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_PRODUCT']._serialized_start=62
  _globals['_PRODUCT']._serialized_end=133
  _globals['_PRODUCTID']._serialized_start=135
  _globals['_PRODUCTID']._serialized_end=161
  _globals['_PRODUCTINFO']._serialized_start=164
  _globals['_PRODUCTINFO']._serialized_end=352
# @@protoc_insertion_point(module_scope)
