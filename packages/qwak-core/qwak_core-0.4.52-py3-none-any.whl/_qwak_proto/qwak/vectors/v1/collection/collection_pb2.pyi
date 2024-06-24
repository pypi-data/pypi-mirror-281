"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.timestamp_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _VectorCollectionStatus:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _VectorCollectionStatusEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_VectorCollectionStatus.ValueType], builtins.type):  # noqa: F821
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    COLLECTION_STATUS_INVALID: _VectorCollectionStatus.ValueType  # 0
    """Invalid collection status"""
    COLLECTION_STATUS_CREATE_REQUESTED: _VectorCollectionStatus.ValueType  # 1
    """Collection create requested"""
    COLLECTION_STATUS_CREATED: _VectorCollectionStatus.ValueType  # 2
    """Collection status is created (exists)"""
    COLLECTION_STATUS_CREATE_FAILED: _VectorCollectionStatus.ValueType  # 3
    """Collection status is created (exists)"""
    COLLECTION_STATUS_DELETE_REQUESTED: _VectorCollectionStatus.ValueType  # 4
    """Collection delete was requested"""
    COLLECTION_STATUS_DELETE_FAILED: _VectorCollectionStatus.ValueType  # 5
    """Collection delete was requested"""
    COLLECTION_STATUS_DELETED: _VectorCollectionStatus.ValueType  # 6
    """Collection was deleted"""

class VectorCollectionStatus(_VectorCollectionStatus, metaclass=_VectorCollectionStatusEnumTypeWrapper): ...

COLLECTION_STATUS_INVALID: VectorCollectionStatus.ValueType  # 0
"""Invalid collection status"""
COLLECTION_STATUS_CREATE_REQUESTED: VectorCollectionStatus.ValueType  # 1
"""Collection create requested"""
COLLECTION_STATUS_CREATED: VectorCollectionStatus.ValueType  # 2
"""Collection status is created (exists)"""
COLLECTION_STATUS_CREATE_FAILED: VectorCollectionStatus.ValueType  # 3
"""Collection status is created (exists)"""
COLLECTION_STATUS_DELETE_REQUESTED: VectorCollectionStatus.ValueType  # 4
"""Collection delete was requested"""
COLLECTION_STATUS_DELETE_FAILED: VectorCollectionStatus.ValueType  # 5
"""Collection delete was requested"""
COLLECTION_STATUS_DELETED: VectorCollectionStatus.ValueType  # 6
"""Collection was deleted"""
global___VectorCollectionStatus = VectorCollectionStatus

class _VectorCollectionMetric:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _VectorCollectionMetricEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_VectorCollectionMetric.ValueType], builtins.type):  # noqa: F821
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    COLLECTION_METRIC_INVALID: _VectorCollectionMetric.ValueType  # 0
    """Collection metric is invalid"""
    COLLECTION_METRIC_L2_SQUARED: _VectorCollectionMetric.ValueType  # 1
    """Collection metric defined L2"""
    COLLECTION_METRIC_COSINE: _VectorCollectionMetric.ValueType  # 2
    """Collection metric defined COSINE"""
    COLLECTION_METRIC_DOT_PRODUCT: _VectorCollectionMetric.ValueType  # 3
    """Collection metric defined DOT PRODUCT"""
    COLLECTION_METRIC_L1: _VectorCollectionMetric.ValueType  # 4
    """Collection metric defined L1"""
    COLLECTION_METRIC_HAMMING: _VectorCollectionMetric.ValueType  # 5
    """Collection metric defined HAMMING"""

class VectorCollectionMetric(_VectorCollectionMetric, metaclass=_VectorCollectionMetricEnumTypeWrapper): ...

COLLECTION_METRIC_INVALID: VectorCollectionMetric.ValueType  # 0
"""Collection metric is invalid"""
COLLECTION_METRIC_L2_SQUARED: VectorCollectionMetric.ValueType  # 1
"""Collection metric defined L2"""
COLLECTION_METRIC_COSINE: VectorCollectionMetric.ValueType  # 2
"""Collection metric defined COSINE"""
COLLECTION_METRIC_DOT_PRODUCT: VectorCollectionMetric.ValueType  # 3
"""Collection metric defined DOT PRODUCT"""
COLLECTION_METRIC_L1: VectorCollectionMetric.ValueType  # 4
"""Collection metric defined L1"""
COLLECTION_METRIC_HAMMING: VectorCollectionMetric.ValueType  # 5
"""Collection metric defined HAMMING"""
global___VectorCollectionMetric = VectorCollectionMetric

class _PropertyType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _PropertyTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_PropertyType.ValueType], builtins.type):  # noqa: F821
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    PROPERTY_TYPE_INVALID: _PropertyType.ValueType  # 0
    PROPERTY_TYPE_STRING: _PropertyType.ValueType  # 1
    PROPERTY_TYPE_INT: _PropertyType.ValueType  # 2
    PROPERTY_TYPE_DOUBLE: _PropertyType.ValueType  # 3
    PROPERTY_TYPE_BOOLEAN: _PropertyType.ValueType  # 4
    PROPERTY_TYPE_TIMESTAMP: _PropertyType.ValueType  # 5

class PropertyType(_PropertyType, metaclass=_PropertyTypeEnumTypeWrapper):
    """DataType of a property in a collection"""

PROPERTY_TYPE_INVALID: PropertyType.ValueType  # 0
PROPERTY_TYPE_STRING: PropertyType.ValueType  # 1
PROPERTY_TYPE_INT: PropertyType.ValueType  # 2
PROPERTY_TYPE_DOUBLE: PropertyType.ValueType  # 3
PROPERTY_TYPE_BOOLEAN: PropertyType.ValueType  # 4
PROPERTY_TYPE_TIMESTAMP: PropertyType.ValueType  # 5
global___PropertyType = PropertyType

class QwakMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CREATED_AT_FIELD_NUMBER: builtins.int
    CREATED_BY_FIELD_NUMBER: builtins.int
    LAST_MODIFIED_AT_FIELD_NUMBER: builtins.int
    LAST_MODIFIED_BY_FIELD_NUMBER: builtins.int
    @property
    def created_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """When the collection was created"""
    created_by: builtins.str
    """User who created the collection"""
    @property
    def last_modified_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """When the collection was last modified"""
    last_modified_by: builtins.str
    """User who modified the collection"""
    def __init__(
        self,
        *,
        created_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        created_by: builtins.str = ...,
        last_modified_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        last_modified_by: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["created_at", b"created_at", "last_modified_at", b"last_modified_at"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["created_at", b"created_at", "created_by", b"created_by", "last_modified_at", b"last_modified_at", "last_modified_by", b"last_modified_by"]) -> None: ...

global___QwakMetadata = QwakMetadata

class VectorCollectionVectorizer(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    QWAK_MODEL_NAME_FIELD_NUMBER: builtins.int
    qwak_model_name: builtins.str
    def __init__(
        self,
        *,
        qwak_model_name: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["qwak_model_name", b"qwak_model_name", "type", b"type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["qwak_model_name", b"qwak_model_name", "type", b"type"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["type", b"type"]) -> typing_extensions.Literal["qwak_model_name"] | None: ...

global___VectorCollectionVectorizer = VectorCollectionVectorizer

class VectorCollectionSpec(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    VECTORIZER_FIELD_NUMBER: builtins.int
    METRIC_FIELD_NUMBER: builtins.int
    DIMENSION_FIELD_NUMBER: builtins.int
    MULTI_TENANCY_ENABLED_FIELD_NUMBER: builtins.int
    name: builtins.str
    """Name of the collection"""
    description: builtins.str
    """User metadata given to this collection"""
    @property
    def vectorizer(self) -> global___VectorCollectionVectorizer:
        """Vectorizing model"""
    metric: global___VectorCollectionMetric.ValueType
    """The metric defined for this collection"""
    dimension: builtins.int
    """Dimension definition for this collection"""
    multi_tenancy_enabled: builtins.bool
    """Whether multi tenancy is enabled for this collection"""
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        description: builtins.str = ...,
        vectorizer: global___VectorCollectionVectorizer | None = ...,
        metric: global___VectorCollectionMetric.ValueType = ...,
        dimension: builtins.int = ...,
        multi_tenancy_enabled: builtins.bool = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["vectorizer", b"vectorizer"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["description", b"description", "dimension", b"dimension", "metric", b"metric", "multi_tenancy_enabled", b"multi_tenancy_enabled", "name", b"name", "vectorizer", b"vectorizer"]) -> None: ...

global___VectorCollectionSpec = VectorCollectionSpec

class VectorCollectionDefinition(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    COLLECTION_SPEC_FIELD_NUMBER: builtins.int
    id: builtins.str
    """The unique ID of the given collection"""
    @property
    def collection_spec(self) -> global___VectorCollectionSpec:
        """The spec details of the collection"""
    def __init__(
        self,
        *,
        id: builtins.str = ...,
        collection_spec: global___VectorCollectionSpec | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["collection_spec", b"collection_spec"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["collection_spec", b"collection_spec", "id", b"id"]) -> None: ...

global___VectorCollectionDefinition = VectorCollectionDefinition

class VectorCollection(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    METADATA_FIELD_NUMBER: builtins.int
    DEFINITION_FIELD_NUMBER: builtins.int
    STATUS_FIELD_NUMBER: builtins.int
    @property
    def metadata(self) -> global___QwakMetadata:
        """QWAK generated metadata of the collection"""
    @property
    def definition(self) -> global___VectorCollectionDefinition:
        """Definition of the collection"""
    status: global___VectorCollectionStatus.ValueType
    """Status of the given collection"""
    def __init__(
        self,
        *,
        metadata: global___QwakMetadata | None = ...,
        definition: global___VectorCollectionDefinition | None = ...,
        status: global___VectorCollectionStatus.ValueType = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["definition", b"definition", "metadata", b"metadata"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["definition", b"definition", "metadata", b"metadata", "status", b"status"]) -> None: ...

global___VectorCollection = VectorCollection

class Property(google.protobuf.message.Message):
    """a property in a collection"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    DATA_TYPE_FIELD_NUMBER: builtins.int
    name: builtins.str
    """property name"""
    data_type: global___PropertyType.ValueType
    """property type"""
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        data_type: global___PropertyType.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["data_type", b"data_type", "name", b"name"]) -> None: ...

global___Property = Property

class CollectionMetadata(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NUM_VECTORS_FIELD_NUMBER: builtins.int
    PROPERTIES_FIELD_NUMBER: builtins.int
    num_vectors: builtins.int
    @property
    def properties(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Property]: ...
    def __init__(
        self,
        *,
        num_vectors: builtins.int = ...,
        properties: collections.abc.Iterable[global___Property] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["num_vectors", b"num_vectors", "properties", b"properties"]) -> None: ...

global___CollectionMetadata = CollectionMetadata
