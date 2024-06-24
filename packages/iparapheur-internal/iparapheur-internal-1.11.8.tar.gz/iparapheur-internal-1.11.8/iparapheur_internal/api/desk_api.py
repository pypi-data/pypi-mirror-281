# coding: utf-8

"""
    iparapheur

    iparapheur v5.x main core application.  The main link between every sub-services, integrating business code logic. 

    The version of the OpenAPI document: DEVELOP
    Contact: iparapheur@libriciel.coop
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501

import warnings
from pydantic import validate_call, Field, StrictFloat, StrictStr, StrictInt
from typing import Any, Dict, List, Optional, Tuple, Union
from typing_extensions import Annotated

from pydantic import Field, StrictStr
from typing import List, Optional
from typing_extensions import Annotated
from iparapheur_internal.models.page_desk_representation import PageDeskRepresentation

from iparapheur_internal.api_client import ApiClient, RequestSerialized
from iparapheur_internal.api_response import ApiResponse
from iparapheur_internal.rest import RESTResponseType


class DeskApi:
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None) -> None:
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client


    @validate_call
    def get_associated_desks(
        self,
        tenant_id: Annotated[StrictStr, Field(description="Tenant id")],
        desk_id: Annotated[StrictStr, Field(description="Desk id")],
        page: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="Zero-based page index (0..N)")] = None,
        size: Annotated[Optional[Annotated[int, Field(strict=True, ge=1)]], Field(description="The size of the page to be returned")] = None,
        sort: Annotated[Optional[List[StrictStr]], Field(description="Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported.")] = None,
        search_term: Annotated[Optional[StrictStr], Field(description="Searching for a specific desk name")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> PageDeskRepresentation:
        """Get the target desk's associated ones


        :param tenant_id: Tenant id (required)
        :type tenant_id: str
        :param desk_id: Desk id (required)
        :type desk_id: str
        :param page: Zero-based page index (0..N)
        :type page: int
        :param size: The size of the page to be returned
        :type size: int
        :param sort: Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported.
        :type sort: List[str]
        :param search_term: Searching for a specific desk name
        :type search_term: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_associated_desks_serialize(
            tenant_id=tenant_id,
            desk_id=desk_id,
            page=page,
            size=size,
            sort=sort,
            search_term=search_term,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '403': "ErrorResponse",
            '200': "PageDeskRepresentation",
            '401': "ErrorResponse",
            '404': "ErrorResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        ).data


    @validate_call
    def get_associated_desks_with_http_info(
        self,
        tenant_id: Annotated[StrictStr, Field(description="Tenant id")],
        desk_id: Annotated[StrictStr, Field(description="Desk id")],
        page: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="Zero-based page index (0..N)")] = None,
        size: Annotated[Optional[Annotated[int, Field(strict=True, ge=1)]], Field(description="The size of the page to be returned")] = None,
        sort: Annotated[Optional[List[StrictStr]], Field(description="Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported.")] = None,
        search_term: Annotated[Optional[StrictStr], Field(description="Searching for a specific desk name")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> ApiResponse[PageDeskRepresentation]:
        """Get the target desk's associated ones


        :param tenant_id: Tenant id (required)
        :type tenant_id: str
        :param desk_id: Desk id (required)
        :type desk_id: str
        :param page: Zero-based page index (0..N)
        :type page: int
        :param size: The size of the page to be returned
        :type size: int
        :param sort: Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported.
        :type sort: List[str]
        :param search_term: Searching for a specific desk name
        :type search_term: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_associated_desks_serialize(
            tenant_id=tenant_id,
            desk_id=desk_id,
            page=page,
            size=size,
            sort=sort,
            search_term=search_term,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '403': "ErrorResponse",
            '200': "PageDeskRepresentation",
            '401': "ErrorResponse",
            '404': "ErrorResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        response_data.read()
        return self.api_client.response_deserialize(
            response_data=response_data,
            response_types_map=_response_types_map,
        )


    @validate_call
    def get_associated_desks_without_preload_content(
        self,
        tenant_id: Annotated[StrictStr, Field(description="Tenant id")],
        desk_id: Annotated[StrictStr, Field(description="Desk id")],
        page: Annotated[Optional[Annotated[int, Field(strict=True, ge=0)]], Field(description="Zero-based page index (0..N)")] = None,
        size: Annotated[Optional[Annotated[int, Field(strict=True, ge=1)]], Field(description="The size of the page to be returned")] = None,
        sort: Annotated[Optional[List[StrictStr]], Field(description="Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported.")] = None,
        search_term: Annotated[Optional[StrictStr], Field(description="Searching for a specific desk name")] = None,
        _request_timeout: Union[
            None,
            Annotated[StrictFloat, Field(gt=0)],
            Tuple[
                Annotated[StrictFloat, Field(gt=0)],
                Annotated[StrictFloat, Field(gt=0)]
            ]
        ] = None,
        _request_auth: Optional[Dict[StrictStr, Any]] = None,
        _content_type: Optional[StrictStr] = None,
        _headers: Optional[Dict[StrictStr, Any]] = None,
        _host_index: Annotated[StrictInt, Field(ge=0, le=0)] = 0,
    ) -> RESTResponseType:
        """Get the target desk's associated ones


        :param tenant_id: Tenant id (required)
        :type tenant_id: str
        :param desk_id: Desk id (required)
        :type desk_id: str
        :param page: Zero-based page index (0..N)
        :type page: int
        :param size: The size of the page to be returned
        :type size: int
        :param sort: Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported.
        :type sort: List[str]
        :param search_term: Searching for a specific desk name
        :type search_term: str
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :type _request_timeout: int, tuple(int, int), optional
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the
                              authentication in the spec for a single request.
        :type _request_auth: dict, optional
        :param _content_type: force content-type for the request.
        :type _content_type: str, Optional
        :param _headers: set to override the headers for a single
                         request; this effectively ignores the headers
                         in the spec for a single request.
        :type _headers: dict, optional
        :param _host_index: set to override the host_index for a single
                            request; this effectively ignores the host_index
                            in the spec for a single request.
        :type _host_index: int, optional
        :return: Returns the result object.
        """ # noqa: E501

        _param = self._get_associated_desks_serialize(
            tenant_id=tenant_id,
            desk_id=desk_id,
            page=page,
            size=size,
            sort=sort,
            search_term=search_term,
            _request_auth=_request_auth,
            _content_type=_content_type,
            _headers=_headers,
            _host_index=_host_index
        )

        _response_types_map: Dict[str, Optional[str]] = {
            '403': "ErrorResponse",
            '200': "PageDeskRepresentation",
            '401': "ErrorResponse",
            '404': "ErrorResponse",
        }
        response_data = self.api_client.call_api(
            *_param,
            _request_timeout=_request_timeout
        )
        return response_data.response


    def _get_associated_desks_serialize(
        self,
        tenant_id,
        desk_id,
        page,
        size,
        sort,
        search_term,
        _request_auth,
        _content_type,
        _headers,
        _host_index,
    ) -> RequestSerialized:

        _host = None

        _collection_formats: Dict[str, str] = {
            'sort': 'multi',
        }

        _path_params: Dict[str, str] = {}
        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] = _headers or {}
        _form_params: List[Tuple[str, str]] = []
        _files: Dict[str, str] = {}
        _body_params: Optional[bytes] = None

        # process the path parameters
        if tenant_id is not None:
            _path_params['tenantId'] = tenant_id
        if desk_id is not None:
            _path_params['deskId'] = desk_id
        # process the query parameters
        if page is not None:
            
            _query_params.append(('page', page))
            
        if size is not None:
            
            _query_params.append(('size', size))
            
        if sort is not None:
            
            _query_params.append(('sort', sort))
            
        if search_term is not None:
            
            _query_params.append(('searchTerm', search_term))
            
        # process the header parameters
        # process the form parameters
        # process the body parameter


        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            [
                'application/json'
            ]
        )


        # authentication setting
        _auth_settings: List[str] = [
            'spring_oauth'
        ]

        return self.api_client.param_serialize(
            method='GET',
            resource_path='/api/internal/tenant/{tenantId}/desk/{deskId}/associatedDesks',
            path_params=_path_params,
            query_params=_query_params,
            header_params=_header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            auth_settings=_auth_settings,
            collection_formats=_collection_formats,
            _host=_host,
            _request_auth=_request_auth
        )


