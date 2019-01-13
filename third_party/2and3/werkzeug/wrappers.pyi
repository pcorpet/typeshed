from datetime import datetime
from typing import (
    Any, Callable, Iterable, Iterator, Mapping, MutableMapping, Optional, Sequence, Text, Tuple, Type, TypeVar, Union,
)

from wsgiref.types import WSGIEnvironment, InputStream

from .datastructures import (
    Authorization, CombinedMultiDict, EnvironHeaders, Headers, ImmutableMultiDict,
    MultiDict, ImmutableTypeConversionDict, HeaderSet,
    Accept, MIMEAccept, CharsetAccept, LanguageAccept,
)

class BaseRequest:
    charset = ...  # type: str
    encoding_errors = ...  # type: str
    max_content_length = ...  # type: Optional[int]
    max_form_memory_size = ...  # type: int
    parameter_storage_class = ...  # type: Type
    list_storage_class = ...  # type: Type
    dict_storage_class = ...  # type: Type
    form_data_parser_class = ...  # type: Type
    trusted_hosts = ...  # type: Optional[Sequence[Text]]
    disable_data_descriptor = ...  # type: Any
    environ: WSGIEnvironment = ...
    shallow = ...  # type: Any
    def __init__(self, environ: WSGIEnvironment, populate_request: bool = ..., shallow: bool = ...) -> None: ...
    @property
    def url_charset(self) -> str: ...
    @classmethod
    def from_values(cls, *args, **kwargs) -> BaseRequest: ...
    @classmethod
    def application(cls, f): ...
    @property
    def want_form_data_parsed(self): ...
    def make_form_data_parser(self): ...
    def close(self) -> None: ...
    def __enter__(self): ...
    def __exit__(self, exc_type, exc_value, tb): ...
    @property
    def stream(self) -> InputStream: ...
    input_stream: InputStream
    args = ...  # type: ImmutableMultiDict
    @property
    def data(self) -> bytes: ...
    def get_data(self, cache: bool = ..., as_text: bool = ..., parse_form_data: bool = ...) -> bytes: ...
    form = ...  # type: ImmutableMultiDict
    values = ...  # type: CombinedMultiDict
    files = ...  # type: MultiDict
    @property
    def cookies(self) -> ImmutableTypeConversionDict[str, str]: ...
    headers = ...  # type: EnvironHeaders
    path = ...  # type: Text
    full_path = ...  # type: Text
    script_root = ...  # type: Text
    url = ...  # type: Text
    base_url = ...  # type: Text
    url_root = ...  # type: Text
    host_url = ...  # type: Text
    host = ...  # type: Text
    query_string = ...  # type: bytes
    method = ...  # type: Text
    def access_route(self): ...
    @property
    def remote_addr(self) -> str: ...
    remote_user = ...  # type: Text
    scheme = ...  # type: str
    is_xhr = ...  # type: bool
    is_secure = ...  # type: bool
    is_multithread = ...  # type: bool
    is_multiprocess = ...  # type: bool
    is_run_once = ...  # type: bool

_OnCloseT = TypeVar('_OnCloseT', bound=Callable[[], Any])
_SelfT = TypeVar('_SelfT', bound=BaseResponse)

class BaseResponse:
    charset = ...  # type: str
    default_status = ...  # type: int
    default_mimetype = ...  # type: str
    implicit_sequence_conversion = ...  # type: bool
    autocorrect_location_header = ...  # type: bool
    automatically_set_content_length = ...  # type: bool
    headers = ...  # type: Headers
    status_code = ...  # type: int
    status = ...  # type: str
    direct_passthrough = ...  # type: bool
    response = ...  # type: Iterable[bytes]
    def __init__(self, response: Optional[Union[str, bytes, bytearray, Iterable[str], Iterable[bytes]]] = ...,
                 status: Optional[Union[Text, int]] = ...,
                 headers: Optional[Union[Headers,
                                         Mapping[Text, Text],
                                         Sequence[Tuple[Text, Text]]]] = ...,
                 mimetype: Optional[Text] = ...,
                 content_type: Optional[Text] = ...,
                 direct_passthrough: bool = ...) -> None: ...
    def call_on_close(self, func: _OnCloseT) -> _OnCloseT: ...
    @classmethod
    def force_type(cls: Type[_SelfT], response: object, environ: Optional[WSGIEnvironment] = ...) -> _SelfT: ...
    @classmethod
    def from_app(cls: Type[_SelfT], app: Any, environ: WSGIEnvironment, buffered: bool = ...) -> _SelfT: ...
    def get_data(self, as_text: bool = ...) -> Any: ...  # returns bytes if as_text is False (the default), else Text
    def set_data(self, value: Union[bytes, Text]) -> None: ...
    data = ...  # type: Any
    def calculate_content_length(self) -> Optional[int]: ...
    def make_sequence(self) -> None: ...
    def iter_encoded(self) -> Iterator[bytes]: ...
    def set_cookie(self, key, value: str = ..., max_age: Optional[Any] = ..., expires: Optional[Any] = ...,
                   path: str = ..., domain: Optional[Any] = ..., secure: bool = ..., httponly: bool = ...): ...
    def delete_cookie(self, key, path: str = ..., domain: Optional[Any] = ...): ...
    @property
    def is_streamed(self) -> bool: ...
    @property
    def is_sequence(self) -> bool: ...
    def close(self) -> None: ...
    def __enter__(self): ...
    def __exit__(self, exc_type, exc_value, tb): ...
    # The no_etag argument if fictional, but required for compatibility with
    # ETagResponseMixin
    def freeze(self, no_etag: bool = ...) -> None: ...
    def get_wsgi_headers(self, environ): ...
    def get_app_iter(self, environ): ...
    def get_wsgi_response(self, environ): ...
    def __call__(self, environ, start_response): ...

class AcceptMixin(object):
    @property
    def accept_mimetypes(self) -> MIMEAccept: ...
    @property
    def accept_charsets(self) -> CharsetAccept: ...
    @property
    def accept_encodings(self) -> Accept: ...
    @property
    def accept_languages(self) -> LanguageAccept: ...

class ETagRequestMixin:
    def cache_control(self): ...
    def if_match(self): ...
    def if_none_match(self): ...
    def if_modified_since(self): ...
    def if_unmodified_since(self): ...
    def if_range(self): ...
    def range(self): ...

class UserAgentMixin:
    def user_agent(self): ...

class AuthorizationMixin:
    @property
    def authorization(self) -> Optional[Authorization]: ...

class StreamOnlyMixin:
    disable_data_descriptor = ...  # type: Any
    want_form_data_parsed = ...  # type: Any

class ETagResponseMixin:
    @property
    def cache_control(self): ...
    status_code = ...  # type: Any
    def make_conditional(self, request_or_environ, accept_ranges: bool = ..., complete_length: Optional[Any] = ...): ...
    def add_etag(self, overwrite: bool = ..., weak: bool = ...): ...
    def set_etag(self, etag, weak: bool = ...): ...
    def get_etag(self): ...
    def freeze(self, no_etag: bool = ...) -> None: ...
    accept_ranges = ...  # type: Any
    content_range = ...  # type: Any

class ResponseStream:
    mode = ...  # type: Any
    response = ...  # type: Any
    closed = ...  # type: Any
    def __init__(self, response): ...
    def write(self, value): ...
    def writelines(self, seq): ...
    def close(self): ...
    def flush(self): ...
    def isatty(self): ...
    @property
    def encoding(self): ...

class ResponseStreamMixin:
    @property
    def stream(self) -> ResponseStream: ...

class CommonRequestDescriptorsMixin:
    @property
    def content_type(self) -> Optional[str]: ...
    @property
    def content_length(self) -> Optional[int]: ...
    @property
    def content_encoding(self) -> Optional[str]: ...
    @property
    def content_md5(self) -> Optional[str]: ...
    @property
    def referrer(self) -> Optional[str]: ...
    @property
    def date(self) -> Optional[datetime]: ...
    @property
    def max_forwards(self) -> Optional[int]: ...
    @property
    def mimetype(self) -> str: ...
    @property
    def mimetype_params(self) -> Mapping[str, str]: ...
    @property
    def pragma(self) -> HeaderSet: ...

class CommonResponseDescriptorsMixin:
    mimetype: Optional[str] = ...
    @property
    def mimetype_params(self) -> MutableMapping[str, str]: ...
    location: Optional[str] = ...
    age: Any = ...  # get: Optional[datetime.timedelta]
    content_type: Optional[str] = ...
    content_length: Optional[int] = ...
    content_location: Optional[str] = ...
    content_encoding: Optional[str] = ...
    content_md5: Optional[str] = ...
    date: Any = ...  # get: Optional[datetime.datetime]
    expires: Any = ...  # get: Optional[datetime.datetime]
    last_modified: Any = ...  # get: Optional[datetime.datetime]
    retry_after: Any = ...  # get: Optional[datetime.datetime]
    vary: Optional[str] = ...
    content_language: Optional[str] = ...
    allow: Optional[str] = ...

class WWWAuthenticateMixin:
    @property
    def www_authenticate(self): ...

class Request(BaseRequest, AcceptMixin, ETagRequestMixin, UserAgentMixin, AuthorizationMixin, CommonRequestDescriptorsMixin): ...
class PlainRequest(StreamOnlyMixin, Request): ...
class Response(BaseResponse, ETagResponseMixin, ResponseStreamMixin, CommonResponseDescriptorsMixin, WWWAuthenticateMixin): ...
