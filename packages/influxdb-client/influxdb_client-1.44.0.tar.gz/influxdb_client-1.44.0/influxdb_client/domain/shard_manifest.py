# coding: utf-8

"""
InfluxDB OSS API Service.

The InfluxDB v2 API provides a programmatic interface for all interactions with InfluxDB. Access the InfluxDB API using the `/api/v2/` endpoint.   # noqa: E501

OpenAPI spec version: 2.0.0
Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401


class ShardManifest(object):
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
        'id': 'int',
        'shard_owners': 'list[ShardOwner]'
    }

    attribute_map = {
        'id': 'id',
        'shard_owners': 'shardOwners'
    }

    def __init__(self, id=None, shard_owners=None):  # noqa: E501,D401,D403
        """ShardManifest - a model defined in OpenAPI."""  # noqa: E501
        self._id = None
        self._shard_owners = None
        self.discriminator = None

        self.id = id
        self.shard_owners = shard_owners

    @property
    def id(self):
        """Get the id of this ShardManifest.

        :return: The id of this ShardManifest.
        :rtype: int
        """  # noqa: E501
        return self._id

    @id.setter
    def id(self, id):
        """Set the id of this ShardManifest.

        :param id: The id of this ShardManifest.
        :type: int
        """  # noqa: E501
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501
        self._id = id

    @property
    def shard_owners(self):
        """Get the shard_owners of this ShardManifest.

        :return: The shard_owners of this ShardManifest.
        :rtype: list[ShardOwner]
        """  # noqa: E501
        return self._shard_owners

    @shard_owners.setter
    def shard_owners(self, shard_owners):
        """Set the shard_owners of this ShardManifest.

        :param shard_owners: The shard_owners of this ShardManifest.
        :type: list[ShardOwner]
        """  # noqa: E501
        if shard_owners is None:
            raise ValueError("Invalid value for `shard_owners`, must not be `None`")  # noqa: E501
        self._shard_owners = shard_owners

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
        if not isinstance(other, ShardManifest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return true if both objects are not equal."""
        return not self == other
