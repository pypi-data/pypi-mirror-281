# coding: utf-8

"""
InfluxDB OSS API Service.

The InfluxDB v2 API provides a programmatic interface for all interactions with InfluxDB. Access the InfluxDB API using the `/api/v2/` endpoint.   # noqa: E501

OpenAPI spec version: 2.0.0
Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401


class Replication(object):
    """NOTE: This class is auto generated by OpenAPI Generator.

    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'id': 'str',
        'name': 'str',
        'description': 'str',
        'org_id': 'str',
        'remote_id': 'str',
        'local_bucket_id': 'str',
        'remote_bucket_id': 'str',
        'remote_bucket_name': 'str',
        'max_queue_size_bytes': 'int',
        'current_queue_size_bytes': 'int',
        'remaining_bytes_to_be_synced': 'int',
        'latest_response_code': 'int',
        'latest_error_message': 'str',
        'drop_non_retryable_data': 'bool'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'description': 'description',
        'org_id': 'orgID',
        'remote_id': 'remoteID',
        'local_bucket_id': 'localBucketID',
        'remote_bucket_id': 'remoteBucketID',
        'remote_bucket_name': 'remoteBucketName',
        'max_queue_size_bytes': 'maxQueueSizeBytes',
        'current_queue_size_bytes': 'currentQueueSizeBytes',
        'remaining_bytes_to_be_synced': 'remainingBytesToBeSynced',
        'latest_response_code': 'latestResponseCode',
        'latest_error_message': 'latestErrorMessage',
        'drop_non_retryable_data': 'dropNonRetryableData'
    }

    def __init__(self, id=None, name=None, description=None, org_id=None, remote_id=None, local_bucket_id=None, remote_bucket_id=None, remote_bucket_name=None, max_queue_size_bytes=None, current_queue_size_bytes=None, remaining_bytes_to_be_synced=None, latest_response_code=None, latest_error_message=None, drop_non_retryable_data=None):  # noqa: E501,D401,D403
        """Replication - a model defined in OpenAPI."""  # noqa: E501
        self._id = None
        self._name = None
        self._description = None
        self._org_id = None
        self._remote_id = None
        self._local_bucket_id = None
        self._remote_bucket_id = None
        self._remote_bucket_name = None
        self._max_queue_size_bytes = None
        self._current_queue_size_bytes = None
        self._remaining_bytes_to_be_synced = None
        self._latest_response_code = None
        self._latest_error_message = None
        self._drop_non_retryable_data = None
        self.discriminator = None

        self.id = id
        self.name = name
        if description is not None:
            self.description = description
        self.org_id = org_id
        self.remote_id = remote_id
        self.local_bucket_id = local_bucket_id
        if remote_bucket_id is not None:
            self.remote_bucket_id = remote_bucket_id
        if remote_bucket_name is not None:
            self.remote_bucket_name = remote_bucket_name
        self.max_queue_size_bytes = max_queue_size_bytes
        if current_queue_size_bytes is not None:
            self.current_queue_size_bytes = current_queue_size_bytes
        if remaining_bytes_to_be_synced is not None:
            self.remaining_bytes_to_be_synced = remaining_bytes_to_be_synced
        if latest_response_code is not None:
            self.latest_response_code = latest_response_code
        if latest_error_message is not None:
            self.latest_error_message = latest_error_message
        if drop_non_retryable_data is not None:
            self.drop_non_retryable_data = drop_non_retryable_data

    @property
    def id(self):
        """Get the id of this Replication.

        :return: The id of this Replication.
        :rtype: str
        """  # noqa: E501
        return self._id

    @id.setter
    def id(self, id):
        """Set the id of this Replication.

        :param id: The id of this Replication.
        :type: str
        """  # noqa: E501
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501
        self._id = id

    @property
    def name(self):
        """Get the name of this Replication.

        :return: The name of this Replication.
        :rtype: str
        """  # noqa: E501
        return self._name

    @name.setter
    def name(self, name):
        """Set the name of this Replication.

        :param name: The name of this Replication.
        :type: str
        """  # noqa: E501
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        self._name = name

    @property
    def description(self):
        """Get the description of this Replication.

        :return: The description of this Replication.
        :rtype: str
        """  # noqa: E501
        return self._description

    @description.setter
    def description(self, description):
        """Set the description of this Replication.

        :param description: The description of this Replication.
        :type: str
        """  # noqa: E501
        self._description = description

    @property
    def org_id(self):
        """Get the org_id of this Replication.

        :return: The org_id of this Replication.
        :rtype: str
        """  # noqa: E501
        return self._org_id

    @org_id.setter
    def org_id(self, org_id):
        """Set the org_id of this Replication.

        :param org_id: The org_id of this Replication.
        :type: str
        """  # noqa: E501
        if org_id is None:
            raise ValueError("Invalid value for `org_id`, must not be `None`")  # noqa: E501
        self._org_id = org_id

    @property
    def remote_id(self):
        """Get the remote_id of this Replication.

        :return: The remote_id of this Replication.
        :rtype: str
        """  # noqa: E501
        return self._remote_id

    @remote_id.setter
    def remote_id(self, remote_id):
        """Set the remote_id of this Replication.

        :param remote_id: The remote_id of this Replication.
        :type: str
        """  # noqa: E501
        if remote_id is None:
            raise ValueError("Invalid value for `remote_id`, must not be `None`")  # noqa: E501
        self._remote_id = remote_id

    @property
    def local_bucket_id(self):
        """Get the local_bucket_id of this Replication.

        :return: The local_bucket_id of this Replication.
        :rtype: str
        """  # noqa: E501
        return self._local_bucket_id

    @local_bucket_id.setter
    def local_bucket_id(self, local_bucket_id):
        """Set the local_bucket_id of this Replication.

        :param local_bucket_id: The local_bucket_id of this Replication.
        :type: str
        """  # noqa: E501
        if local_bucket_id is None:
            raise ValueError("Invalid value for `local_bucket_id`, must not be `None`")  # noqa: E501
        self._local_bucket_id = local_bucket_id

    @property
    def remote_bucket_id(self):
        """Get the remote_bucket_id of this Replication.

        :return: The remote_bucket_id of this Replication.
        :rtype: str
        """  # noqa: E501
        return self._remote_bucket_id

    @remote_bucket_id.setter
    def remote_bucket_id(self, remote_bucket_id):
        """Set the remote_bucket_id of this Replication.

        :param remote_bucket_id: The remote_bucket_id of this Replication.
        :type: str
        """  # noqa: E501
        self._remote_bucket_id = remote_bucket_id

    @property
    def remote_bucket_name(self):
        """Get the remote_bucket_name of this Replication.

        :return: The remote_bucket_name of this Replication.
        :rtype: str
        """  # noqa: E501
        return self._remote_bucket_name

    @remote_bucket_name.setter
    def remote_bucket_name(self, remote_bucket_name):
        """Set the remote_bucket_name of this Replication.

        :param remote_bucket_name: The remote_bucket_name of this Replication.
        :type: str
        """  # noqa: E501
        self._remote_bucket_name = remote_bucket_name

    @property
    def max_queue_size_bytes(self):
        """Get the max_queue_size_bytes of this Replication.

        :return: The max_queue_size_bytes of this Replication.
        :rtype: int
        """  # noqa: E501
        return self._max_queue_size_bytes

    @max_queue_size_bytes.setter
    def max_queue_size_bytes(self, max_queue_size_bytes):
        """Set the max_queue_size_bytes of this Replication.

        :param max_queue_size_bytes: The max_queue_size_bytes of this Replication.
        :type: int
        """  # noqa: E501
        if max_queue_size_bytes is None:
            raise ValueError("Invalid value for `max_queue_size_bytes`, must not be `None`")  # noqa: E501
        self._max_queue_size_bytes = max_queue_size_bytes

    @property
    def current_queue_size_bytes(self):
        """Get the current_queue_size_bytes of this Replication.

        :return: The current_queue_size_bytes of this Replication.
        :rtype: int
        """  # noqa: E501
        return self._current_queue_size_bytes

    @current_queue_size_bytes.setter
    def current_queue_size_bytes(self, current_queue_size_bytes):
        """Set the current_queue_size_bytes of this Replication.

        :param current_queue_size_bytes: The current_queue_size_bytes of this Replication.
        :type: int
        """  # noqa: E501
        self._current_queue_size_bytes = current_queue_size_bytes

    @property
    def remaining_bytes_to_be_synced(self):
        """Get the remaining_bytes_to_be_synced of this Replication.

        :return: The remaining_bytes_to_be_synced of this Replication.
        :rtype: int
        """  # noqa: E501
        return self._remaining_bytes_to_be_synced

    @remaining_bytes_to_be_synced.setter
    def remaining_bytes_to_be_synced(self, remaining_bytes_to_be_synced):
        """Set the remaining_bytes_to_be_synced of this Replication.

        :param remaining_bytes_to_be_synced: The remaining_bytes_to_be_synced of this Replication.
        :type: int
        """  # noqa: E501
        self._remaining_bytes_to_be_synced = remaining_bytes_to_be_synced

    @property
    def latest_response_code(self):
        """Get the latest_response_code of this Replication.

        :return: The latest_response_code of this Replication.
        :rtype: int
        """  # noqa: E501
        return self._latest_response_code

    @latest_response_code.setter
    def latest_response_code(self, latest_response_code):
        """Set the latest_response_code of this Replication.

        :param latest_response_code: The latest_response_code of this Replication.
        :type: int
        """  # noqa: E501
        self._latest_response_code = latest_response_code

    @property
    def latest_error_message(self):
        """Get the latest_error_message of this Replication.

        :return: The latest_error_message of this Replication.
        :rtype: str
        """  # noqa: E501
        return self._latest_error_message

    @latest_error_message.setter
    def latest_error_message(self, latest_error_message):
        """Set the latest_error_message of this Replication.

        :param latest_error_message: The latest_error_message of this Replication.
        :type: str
        """  # noqa: E501
        self._latest_error_message = latest_error_message

    @property
    def drop_non_retryable_data(self):
        """Get the drop_non_retryable_data of this Replication.

        :return: The drop_non_retryable_data of this Replication.
        :rtype: bool
        """  # noqa: E501
        return self._drop_non_retryable_data

    @drop_non_retryable_data.setter
    def drop_non_retryable_data(self, drop_non_retryable_data):
        """Set the drop_non_retryable_data of this Replication.

        :param drop_non_retryable_data: The drop_non_retryable_data of this Replication.
        :type: bool
        """  # noqa: E501
        self._drop_non_retryable_data = drop_non_retryable_data

    def to_dict(self):
        """Return the model properties as a dict."""
        result = {}

        for attr, _ in self.openapi_types.items():
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Return the string representation of the model."""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`."""
        return self.to_str()

    def __eq__(self, other):
        """Return true if both objects are equal."""
        if not isinstance(other, Replication):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return true if both objects are not equal."""
        return not self == other
