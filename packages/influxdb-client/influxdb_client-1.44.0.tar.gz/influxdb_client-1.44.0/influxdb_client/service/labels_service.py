# coding: utf-8

"""
InfluxDB OSS API Service.

The InfluxDB v2 API provides a programmatic interface for all interactions with InfluxDB. Access the InfluxDB API using the `/api/v2/` endpoint.   # noqa: E501

OpenAPI spec version: 2.0.0
Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

from influxdb_client.service._base_service import _BaseService


class LabelsService(_BaseService):
    """NOTE: This class is auto generated by OpenAPI Generator.

    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):  # noqa: E501,D401,D403
        """LabelsService - a operation defined in OpenAPI."""
        super().__init__(api_client)

    def delete_labels_id(self, label_id, **kwargs):  # noqa: E501,D401,D403
        """Delete a label.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_labels_id(label_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str label_id: The ID of the label to delete. (required)
        :param str zap_trace_span: OpenTracing span context
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """  # noqa: E501
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_labels_id_with_http_info(label_id, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_labels_id_with_http_info(label_id, **kwargs)  # noqa: E501
            return data

    def delete_labels_id_with_http_info(self, label_id, **kwargs):  # noqa: E501,D401,D403
        """Delete a label.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_labels_id_with_http_info(label_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str label_id: The ID of the label to delete. (required)
        :param str zap_trace_span: OpenTracing span context
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """  # noqa: E501
        local_var_params, path_params, query_params, header_params, body_params = \
            self._delete_labels_id_prepare(label_id, **kwargs)  # noqa: E501

        return self.api_client.call_api(
            '/api/v2/labels/{labelID}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=[],
            files={},
            response_type=None,  # noqa: E501
            auth_settings=[],
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats={},
            urlopen_kw=kwargs.get('urlopen_kw', None))

    async def delete_labels_id_async(self, label_id, **kwargs):  # noqa: E501,D401,D403
        """Delete a label.

        This method makes an asynchronous HTTP request.

        :param async_req bool
        :param str label_id: The ID of the label to delete. (required)
        :param str zap_trace_span: OpenTracing span context
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """  # noqa: E501
        local_var_params, path_params, query_params, header_params, body_params = \
            self._delete_labels_id_prepare(label_id, **kwargs)  # noqa: E501

        return await self.api_client.call_api(
            '/api/v2/labels/{labelID}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=[],
            files={},
            response_type=None,  # noqa: E501
            auth_settings=[],
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats={},
            urlopen_kw=kwargs.get('urlopen_kw', None))

    def _delete_labels_id_prepare(self, label_id, **kwargs):  # noqa: E501,D401,D403
        local_var_params = locals()

        all_params = ['label_id', 'zap_trace_span']  # noqa: E501
        self._check_operation_params('delete_labels_id', all_params, local_var_params)
        # verify the required parameter 'label_id' is set
        if ('label_id' not in local_var_params or
                local_var_params['label_id'] is None):
            raise ValueError("Missing the required parameter `label_id` when calling `delete_labels_id`")  # noqa: E501

        path_params = {}
        if 'label_id' in local_var_params:
            path_params['labelID'] = local_var_params['label_id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'zap_trace_span' in local_var_params:
            header_params['Zap-Trace-Span'] = local_var_params['zap_trace_span']  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        return local_var_params, path_params, query_params, header_params, body_params

    def get_labels(self, **kwargs):  # noqa: E501,D401,D403
        """List all labels.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_labels(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str zap_trace_span: OpenTracing span context
        :param str org_id: The organization ID.
        :return: LabelsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """  # noqa: E501
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_labels_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_labels_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_labels_with_http_info(self, **kwargs):  # noqa: E501,D401,D403
        """List all labels.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_labels_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str zap_trace_span: OpenTracing span context
        :param str org_id: The organization ID.
        :return: LabelsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """  # noqa: E501
        local_var_params, path_params, query_params, header_params, body_params = \
            self._get_labels_prepare(**kwargs)  # noqa: E501

        return self.api_client.call_api(
            '/api/v2/labels', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=[],
            files={},
            response_type='LabelsResponse',  # noqa: E501
            auth_settings=[],
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats={},
            urlopen_kw=kwargs.get('urlopen_kw', None))

    async def get_labels_async(self, **kwargs):  # noqa: E501,D401,D403
        """List all labels.

        This method makes an asynchronous HTTP request.

        :param async_req bool
        :param str zap_trace_span: OpenTracing span context
        :param str org_id: The organization ID.
        :return: LabelsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """  # noqa: E501
        local_var_params, path_params, query_params, header_params, body_params = \
            self._get_labels_prepare(**kwargs)  # noqa: E501

        return await self.api_client.call_api(
            '/api/v2/labels', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=[],
            files={},
            response_type='LabelsResponse',  # noqa: E501
            auth_settings=[],
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats={},
            urlopen_kw=kwargs.get('urlopen_kw', None))

    def _get_labels_prepare(self, **kwargs):  # noqa: E501,D401,D403
        local_var_params = locals()

        all_params = ['zap_trace_span', 'org_id']  # noqa: E501
        self._check_operation_params('get_labels', all_params, local_var_params)

        path_params = {}

        query_params = []
        if 'org_id' in local_var_params:
            query_params.append(('orgID', local_var_params['org_id']))  # noqa: E501

        header_params = {}
        if 'zap_trace_span' in local_var_params:
            header_params['Zap-Trace-Span'] = local_var_params['zap_trace_span']  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        return local_var_params, path_params, query_params, header_params, body_params

    def get_labels_id(self, label_id, **kwargs):  # noqa: E501,D401,D403
        """Retrieve a label.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_labels_id(label_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str label_id: The ID of the label to update. (required)
        :param str zap_trace_span: OpenTracing span context
        :return: LabelResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """  # noqa: E501
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_labels_id_with_http_info(label_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_labels_id_with_http_info(label_id, **kwargs)  # noqa: E501
            return data

    def get_labels_id_with_http_info(self, label_id, **kwargs):  # noqa: E501,D401,D403
        """Retrieve a label.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_labels_id_with_http_info(label_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str label_id: The ID of the label to update. (required)
        :param str zap_trace_span: OpenTracing span context
        :return: LabelResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """  # noqa: E501
        local_var_params, path_params, query_params, header_params, body_params = \
            self._get_labels_id_prepare(label_id, **kwargs)  # noqa: E501

        return self.api_client.call_api(
            '/api/v2/labels/{labelID}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=[],
            files={},
            response_type='LabelResponse',  # noqa: E501
            auth_settings=[],
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats={},
            urlopen_kw=kwargs.get('urlopen_kw', None))

    async def get_labels_id_async(self, label_id, **kwargs):  # noqa: E501,D401,D403
        """Retrieve a label.

        This method makes an asynchronous HTTP request.

        :param async_req bool
        :param str label_id: The ID of the label to update. (required)
        :param str zap_trace_span: OpenTracing span context
        :return: LabelResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """  # noqa: E501
        local_var_params, path_params, query_params, header_params, body_params = \
            self._get_labels_id_prepare(label_id, **kwargs)  # noqa: E501

        return await self.api_client.call_api(
            '/api/v2/labels/{labelID}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=[],
            files={},
            response_type='LabelResponse',  # noqa: E501
            auth_settings=[],
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats={},
            urlopen_kw=kwargs.get('urlopen_kw', None))

    def _get_labels_id_prepare(self, label_id, **kwargs):  # noqa: E501,D401,D403
        local_var_params = locals()

        all_params = ['label_id', 'zap_trace_span']  # noqa: E501
        self._check_operation_params('get_labels_id', all_params, local_var_params)
        # verify the required parameter 'label_id' is set
        if ('label_id' not in local_var_params or
                local_var_params['label_id'] is None):
            raise ValueError("Missing the required parameter `label_id` when calling `get_labels_id`")  # noqa: E501

        path_params = {}
        if 'label_id' in local_var_params:
            path_params['labelID'] = local_var_params['label_id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'zap_trace_span' in local_var_params:
            header_params['Zap-Trace-Span'] = local_var_params['zap_trace_span']  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        return local_var_params, path_params, query_params, header_params, body_params

    def patch_labels_id(self, label_id, label_update, **kwargs):  # noqa: E501,D401,D403
        """Update a label.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.patch_labels_id(label_id, label_update, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str label_id: The ID of the label to update. (required)
        :param LabelUpdate label_update: A label update. (required)
        :param str zap_trace_span: OpenTracing span context
        :return: LabelResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """  # noqa: E501
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.patch_labels_id_with_http_info(label_id, label_update, **kwargs)  # noqa: E501
        else:
            (data) = self.patch_labels_id_with_http_info(label_id, label_update, **kwargs)  # noqa: E501
            return data

    def patch_labels_id_with_http_info(self, label_id, label_update, **kwargs):  # noqa: E501,D401,D403
        """Update a label.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.patch_labels_id_with_http_info(label_id, label_update, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str label_id: The ID of the label to update. (required)
        :param LabelUpdate label_update: A label update. (required)
        :param str zap_trace_span: OpenTracing span context
        :return: LabelResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """  # noqa: E501
        local_var_params, path_params, query_params, header_params, body_params = \
            self._patch_labels_id_prepare(label_id, label_update, **kwargs)  # noqa: E501

        return self.api_client.call_api(
            '/api/v2/labels/{labelID}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=[],
            files={},
            response_type='LabelResponse',  # noqa: E501
            auth_settings=[],
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats={},
            urlopen_kw=kwargs.get('urlopen_kw', None))

    async def patch_labels_id_async(self, label_id, label_update, **kwargs):  # noqa: E501,D401,D403
        """Update a label.

        This method makes an asynchronous HTTP request.

        :param async_req bool
        :param str label_id: The ID of the label to update. (required)
        :param LabelUpdate label_update: A label update. (required)
        :param str zap_trace_span: OpenTracing span context
        :return: LabelResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """  # noqa: E501
        local_var_params, path_params, query_params, header_params, body_params = \
            self._patch_labels_id_prepare(label_id, label_update, **kwargs)  # noqa: E501

        return await self.api_client.call_api(
            '/api/v2/labels/{labelID}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=[],
            files={},
            response_type='LabelResponse',  # noqa: E501
            auth_settings=[],
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats={},
            urlopen_kw=kwargs.get('urlopen_kw', None))

    def _patch_labels_id_prepare(self, label_id, label_update, **kwargs):  # noqa: E501,D401,D403
        local_var_params = locals()

        all_params = ['label_id', 'label_update', 'zap_trace_span']  # noqa: E501
        self._check_operation_params('patch_labels_id', all_params, local_var_params)
        # verify the required parameter 'label_id' is set
        if ('label_id' not in local_var_params or
                local_var_params['label_id'] is None):
            raise ValueError("Missing the required parameter `label_id` when calling `patch_labels_id`")  # noqa: E501
        # verify the required parameter 'label_update' is set
        if ('label_update' not in local_var_params or
                local_var_params['label_update'] is None):
            raise ValueError("Missing the required parameter `label_update` when calling `patch_labels_id`")  # noqa: E501

        path_params = {}
        if 'label_id' in local_var_params:
            path_params['labelID'] = local_var_params['label_id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'zap_trace_span' in local_var_params:
            header_params['Zap-Trace-Span'] = local_var_params['zap_trace_span']  # noqa: E501

        body_params = None
        if 'label_update' in local_var_params:
            body_params = local_var_params['label_update']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        return local_var_params, path_params, query_params, header_params, body_params

    def post_labels(self, label_create_request, **kwargs):  # noqa: E501,D401,D403
        """Create a label.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.post_labels(label_create_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param LabelCreateRequest label_create_request: The label to create. (required)
        :return: LabelResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """  # noqa: E501
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.post_labels_with_http_info(label_create_request, **kwargs)  # noqa: E501
        else:
            (data) = self.post_labels_with_http_info(label_create_request, **kwargs)  # noqa: E501
            return data

    def post_labels_with_http_info(self, label_create_request, **kwargs):  # noqa: E501,D401,D403
        """Create a label.

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.post_labels_with_http_info(label_create_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param LabelCreateRequest label_create_request: The label to create. (required)
        :return: LabelResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """  # noqa: E501
        local_var_params, path_params, query_params, header_params, body_params = \
            self._post_labels_prepare(label_create_request, **kwargs)  # noqa: E501

        return self.api_client.call_api(
            '/api/v2/labels', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=[],
            files={},
            response_type='LabelResponse',  # noqa: E501
            auth_settings=[],
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats={},
            urlopen_kw=kwargs.get('urlopen_kw', None))

    async def post_labels_async(self, label_create_request, **kwargs):  # noqa: E501,D401,D403
        """Create a label.

        This method makes an asynchronous HTTP request.

        :param async_req bool
        :param LabelCreateRequest label_create_request: The label to create. (required)
        :return: LabelResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """  # noqa: E501
        local_var_params, path_params, query_params, header_params, body_params = \
            self._post_labels_prepare(label_create_request, **kwargs)  # noqa: E501

        return await self.api_client.call_api(
            '/api/v2/labels', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=[],
            files={},
            response_type='LabelResponse',  # noqa: E501
            auth_settings=[],
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats={},
            urlopen_kw=kwargs.get('urlopen_kw', None))

    def _post_labels_prepare(self, label_create_request, **kwargs):  # noqa: E501,D401,D403
        local_var_params = locals()

        all_params = ['label_create_request']  # noqa: E501
        self._check_operation_params('post_labels', all_params, local_var_params)
        # verify the required parameter 'label_create_request' is set
        if ('label_create_request' not in local_var_params or
                local_var_params['label_create_request'] is None):
            raise ValueError("Missing the required parameter `label_create_request` when calling `post_labels`")  # noqa: E501

        path_params = {}

        query_params = []

        header_params = {}

        body_params = None
        if 'label_create_request' in local_var_params:
            body_params = local_var_params['label_create_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        return local_var_params, path_params, query_params, header_params, body_params
