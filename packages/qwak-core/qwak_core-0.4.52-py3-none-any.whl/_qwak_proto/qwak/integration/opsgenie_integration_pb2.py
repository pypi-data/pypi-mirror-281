# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qwak/integration/opsgenie_integration.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+qwak/integration/opsgenie_integration.proto\x12\x1bqwak.integration.management\"\xb7\x02\n\x13OpsgenieIntegration\x12[\n\x1e\x65ncrypted_opsgenie_auth_config\x18\x01 \x01(\x0b\x32/.qwak.integration.management.OpsgenieAuthConfigB\x02\x18\x01\x12H\n\x11opsgenie_settings\x18\x02 \x01(\x0b\x32-.qwak.integration.management.OpsgenieSettings\x12\x10\n\x08\x62\x61se_url\x18\x03 \x01(\t\x12_\n\x17opsgeinie_system_secret\x18\x04 \x01(\x0b\x32<.qwak.integration.management.OpsgeinieSystemSecretDescriptorH\x00\x42\x06\n\x04\x61uth\"\xc3\x01\n\x17OpsgenieIntegrationSpec\x12H\n\x11opsgenie_settings\x18\x02 \x01(\x0b\x32-.qwak.integration.management.OpsgenieSettings\x12V\n\x1bopsgenie_auth_configuration\x18\x03 \x01(\x0b\x32/.qwak.integration.management.OpsgenieAuthConfigH\x00\x42\x06\n\x04\x61uth\"O\n\x10OpsgenieSettings\x12;\n\x06region\x18\x02 \x01(\x0e\x32+.qwak.integration.management.OpsgenieRegion\"%\n\x12OpsgenieAuthConfig\x12\x0f\n\x07\x61pi_key\x18\x01 \x01(\t\"R\n\x1fOpsgeinieSystemSecretDescriptor\x12\x13\n\x0bsecret_name\x18\x01 \x01(\t\x12\x1a\n\x12\x61pi_key_secret_key\x18\x02 \x01(\t\"\xa4\x01\n\x16OpsgenieValidationSpec\x12M\n\x14opsgenie_auth_config\x18\x01 \x01(\x0b\x32/.qwak.integration.management.OpsgenieAuthConfig\x12;\n\x06region\x18\x02 \x01(\x0e\x32+.qwak.integration.management.OpsgenieRegion\"\x1c\n\x1aOpsgenieIntegrationOptions*]\n\x0eOpsgenieRegion\x12\x1b\n\x17OPSGENIE_REGION_INVALID\x10\x00\x12\x16\n\x12OPSGENIE_REGION_US\x10\x01\x12\x16\n\x12OPSGENIE_REGION_EU\x10\x02\x42H\n&com.qwak.ai.management.integration.apiP\x01Z\x1cqwak/integration;integrationb\x06proto3')

_OPSGENIEREGION = DESCRIPTOR.enum_types_by_name['OpsgenieRegion']
OpsgenieRegion = enum_type_wrapper.EnumTypeWrapper(_OPSGENIEREGION)
OPSGENIE_REGION_INVALID = 0
OPSGENIE_REGION_US = 1
OPSGENIE_REGION_EU = 2


_OPSGENIEINTEGRATION = DESCRIPTOR.message_types_by_name['OpsgenieIntegration']
_OPSGENIEINTEGRATIONSPEC = DESCRIPTOR.message_types_by_name['OpsgenieIntegrationSpec']
_OPSGENIESETTINGS = DESCRIPTOR.message_types_by_name['OpsgenieSettings']
_OPSGENIEAUTHCONFIG = DESCRIPTOR.message_types_by_name['OpsgenieAuthConfig']
_OPSGEINIESYSTEMSECRETDESCRIPTOR = DESCRIPTOR.message_types_by_name['OpsgeinieSystemSecretDescriptor']
_OPSGENIEVALIDATIONSPEC = DESCRIPTOR.message_types_by_name['OpsgenieValidationSpec']
_OPSGENIEINTEGRATIONOPTIONS = DESCRIPTOR.message_types_by_name['OpsgenieIntegrationOptions']
OpsgenieIntegration = _reflection.GeneratedProtocolMessageType('OpsgenieIntegration', (_message.Message,), {
  'DESCRIPTOR' : _OPSGENIEINTEGRATION,
  '__module__' : 'qwak.integration.opsgenie_integration_pb2'
  # @@protoc_insertion_point(class_scope:qwak.integration.management.OpsgenieIntegration)
  })
_sym_db.RegisterMessage(OpsgenieIntegration)

OpsgenieIntegrationSpec = _reflection.GeneratedProtocolMessageType('OpsgenieIntegrationSpec', (_message.Message,), {
  'DESCRIPTOR' : _OPSGENIEINTEGRATIONSPEC,
  '__module__' : 'qwak.integration.opsgenie_integration_pb2'
  # @@protoc_insertion_point(class_scope:qwak.integration.management.OpsgenieIntegrationSpec)
  })
_sym_db.RegisterMessage(OpsgenieIntegrationSpec)

OpsgenieSettings = _reflection.GeneratedProtocolMessageType('OpsgenieSettings', (_message.Message,), {
  'DESCRIPTOR' : _OPSGENIESETTINGS,
  '__module__' : 'qwak.integration.opsgenie_integration_pb2'
  # @@protoc_insertion_point(class_scope:qwak.integration.management.OpsgenieSettings)
  })
_sym_db.RegisterMessage(OpsgenieSettings)

OpsgenieAuthConfig = _reflection.GeneratedProtocolMessageType('OpsgenieAuthConfig', (_message.Message,), {
  'DESCRIPTOR' : _OPSGENIEAUTHCONFIG,
  '__module__' : 'qwak.integration.opsgenie_integration_pb2'
  # @@protoc_insertion_point(class_scope:qwak.integration.management.OpsgenieAuthConfig)
  })
_sym_db.RegisterMessage(OpsgenieAuthConfig)

OpsgeinieSystemSecretDescriptor = _reflection.GeneratedProtocolMessageType('OpsgeinieSystemSecretDescriptor', (_message.Message,), {
  'DESCRIPTOR' : _OPSGEINIESYSTEMSECRETDESCRIPTOR,
  '__module__' : 'qwak.integration.opsgenie_integration_pb2'
  # @@protoc_insertion_point(class_scope:qwak.integration.management.OpsgeinieSystemSecretDescriptor)
  })
_sym_db.RegisterMessage(OpsgeinieSystemSecretDescriptor)

OpsgenieValidationSpec = _reflection.GeneratedProtocolMessageType('OpsgenieValidationSpec', (_message.Message,), {
  'DESCRIPTOR' : _OPSGENIEVALIDATIONSPEC,
  '__module__' : 'qwak.integration.opsgenie_integration_pb2'
  # @@protoc_insertion_point(class_scope:qwak.integration.management.OpsgenieValidationSpec)
  })
_sym_db.RegisterMessage(OpsgenieValidationSpec)

OpsgenieIntegrationOptions = _reflection.GeneratedProtocolMessageType('OpsgenieIntegrationOptions', (_message.Message,), {
  'DESCRIPTOR' : _OPSGENIEINTEGRATIONOPTIONS,
  '__module__' : 'qwak.integration.opsgenie_integration_pb2'
  # @@protoc_insertion_point(class_scope:qwak.integration.management.OpsgenieIntegrationOptions)
  })
_sym_db.RegisterMessage(OpsgenieIntegrationOptions)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n&com.qwak.ai.management.integration.apiP\001Z\034qwak/integration;integration'
  _OPSGENIEINTEGRATION.fields_by_name['encrypted_opsgenie_auth_config']._options = None
  _OPSGENIEINTEGRATION.fields_by_name['encrypted_opsgenie_auth_config']._serialized_options = b'\030\001'
  _OPSGENIEREGION._serialized_start=989
  _OPSGENIEREGION._serialized_end=1082
  _OPSGENIEINTEGRATION._serialized_start=77
  _OPSGENIEINTEGRATION._serialized_end=388
  _OPSGENIEINTEGRATIONSPEC._serialized_start=391
  _OPSGENIEINTEGRATIONSPEC._serialized_end=586
  _OPSGENIESETTINGS._serialized_start=588
  _OPSGENIESETTINGS._serialized_end=667
  _OPSGENIEAUTHCONFIG._serialized_start=669
  _OPSGENIEAUTHCONFIG._serialized_end=706
  _OPSGEINIESYSTEMSECRETDESCRIPTOR._serialized_start=708
  _OPSGEINIESYSTEMSECRETDESCRIPTOR._serialized_end=790
  _OPSGENIEVALIDATIONSPEC._serialized_start=793
  _OPSGENIEVALIDATIONSPEC._serialized_end=957
  _OPSGENIEINTEGRATIONOPTIONS._serialized_start=959
  _OPSGENIEINTEGRATIONOPTIONS._serialized_end=987
# @@protoc_insertion_point(module_scope)
