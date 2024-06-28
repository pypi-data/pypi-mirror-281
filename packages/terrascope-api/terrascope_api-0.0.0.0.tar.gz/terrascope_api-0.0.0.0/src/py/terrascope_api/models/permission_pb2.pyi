import common_models_pb2 as _common_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union
from common_models_pb2 import Pagination as Pagination

DESCRIPTOR: _descriptor.FileDescriptor

class Permission(_message.Message):
    __slots__ = ("resource_type", "resource_ids", "subject_ids", "permission_types")
    class ResourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_PERMISSION_RESOURCE_TYPE: _ClassVar[Permission.ResourceType]
        ALGORITHM: _ClassVar[Permission.ResourceType]
        ALGORITHM_COMPUTATION: _ClassVar[Permission.ResourceType]
        ALGORITHM_CONFIG: _ClassVar[Permission.ResourceType]
        ANALYSIS: _ClassVar[Permission.ResourceType]
        ANALYSIS_COMPUTATION: _ClassVar[Permission.ResourceType]
        ANALYSIS_CONFIG: _ClassVar[Permission.ResourceType]
        AOI_COLLECTION: _ClassVar[Permission.ResourceType]
        RESULT: _ClassVar[Permission.ResourceType]
        TOI: _ClassVar[Permission.ResourceType]
    UNKNOWN_PERMISSION_RESOURCE_TYPE: Permission.ResourceType
    ALGORITHM: Permission.ResourceType
    ALGORITHM_COMPUTATION: Permission.ResourceType
    ALGORITHM_CONFIG: Permission.ResourceType
    ANALYSIS: Permission.ResourceType
    ANALYSIS_COMPUTATION: Permission.ResourceType
    ANALYSIS_CONFIG: Permission.ResourceType
    AOI_COLLECTION: Permission.ResourceType
    RESULT: Permission.ResourceType
    TOI: Permission.ResourceType
    class PermissionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_PERMISSION_TYPE: _ClassVar[Permission.PermissionType]
        READ: _ClassVar[Permission.PermissionType]
        WRITE: _ClassVar[Permission.PermissionType]
        ADMIN: _ClassVar[Permission.PermissionType]
    UNKNOWN_PERMISSION_TYPE: Permission.PermissionType
    READ: Permission.PermissionType
    WRITE: Permission.PermissionType
    ADMIN: Permission.PermissionType
    class CollectionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN_COLLECTION_TYPE: _ClassVar[Permission.CollectionType]
        PUBLIC: _ClassVar[Permission.CollectionType]
    UNKNOWN_COLLECTION_TYPE: Permission.CollectionType
    PUBLIC: Permission.CollectionType
    RESOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_IDS_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_IDS_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_TYPES_FIELD_NUMBER: _ClassVar[int]
    resource_type: Permission.ResourceType
    resource_ids: _containers.RepeatedScalarFieldContainer[str]
    subject_ids: _containers.RepeatedScalarFieldContainer[str]
    permission_types: _containers.RepeatedScalarFieldContainer[Permission.PermissionType]
    def __init__(self, resource_type: _Optional[_Union[Permission.ResourceType, str]] = ..., resource_ids: _Optional[_Iterable[str]] = ..., subject_ids: _Optional[_Iterable[str]] = ..., permission_types: _Optional[_Iterable[_Union[Permission.PermissionType, str]]] = ...) -> None: ...

class PermissionCreateRequest(_message.Message):
    __slots__ = ("permissions",)
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    permissions: _containers.RepeatedCompositeFieldContainer[Permission]
    def __init__(self, permissions: _Optional[_Iterable[_Union[Permission, _Mapping]]] = ...) -> None: ...

class PermissionCreateResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...

class PermissionDeleteRequest(_message.Message):
    __slots__ = ("permissions",)
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    permissions: _containers.RepeatedCompositeFieldContainer[Permission]
    def __init__(self, permissions: _Optional[_Iterable[_Union[Permission, _Mapping]]] = ...) -> None: ...

class PermissionDeleteResponse(_message.Message):
    __slots__ = ("status_code",)
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    status_code: int
    def __init__(self, status_code: _Optional[int] = ...) -> None: ...
