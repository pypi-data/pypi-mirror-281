# coding: utf-8

"""
InfluxDB OSS API Service.

The InfluxDB v2 API provides a programmatic interface for all interactions with InfluxDB. Access the InfluxDB API using the `/api/v2/` endpoint.   # noqa: E501

OpenAPI spec version: 2.0.0
Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

from influxdb_client.domain.view_properties import ViewProperties


class MarkdownViewProperties(ViewProperties):
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
        'type': 'str',
        'shape': 'str',
        'note': 'str'
    }

    attribute_map = {
        'type': 'type',
        'shape': 'shape',
        'note': 'note'
    }

    def __init__(self, type=None, shape=None, note=None):  # noqa: E501,D401,D403
        """MarkdownViewProperties - a model defined in OpenAPI."""  # noqa: E501
        ViewProperties.__init__(self)  # noqa: E501

        self._type = None
        self._shape = None
        self._note = None
        self.discriminator = None

        self.type = type
        self.shape = shape
        self.note = note

    @property
    def type(self):
        """Get the type of this MarkdownViewProperties.

        :return: The type of this MarkdownViewProperties.
        :rtype: str
        """  # noqa: E501
        return self._type

    @type.setter
    def type(self, type):
        """Set the type of this MarkdownViewProperties.

        :param type: The type of this MarkdownViewProperties.
        :type: str
        """  # noqa: E501
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        self._type = type

    @property
    def shape(self):
        """Get the shape of this MarkdownViewProperties.

        :return: The shape of this MarkdownViewProperties.
        :rtype: str
        """  # noqa: E501
        return self._shape

    @shape.setter
    def shape(self, shape):
        """Set the shape of this MarkdownViewProperties.

        :param shape: The shape of this MarkdownViewProperties.
        :type: str
        """  # noqa: E501
        if shape is None:
            raise ValueError("Invalid value for `shape`, must not be `None`")  # noqa: E501
        self._shape = shape

    @property
    def note(self):
        """Get the note of this MarkdownViewProperties.

        :return: The note of this MarkdownViewProperties.
        :rtype: str
        """  # noqa: E501
        return self._note

    @note.setter
    def note(self, note):
        """Set the note of this MarkdownViewProperties.

        :param note: The note of this MarkdownViewProperties.
        :type: str
        """  # noqa: E501
        if note is None:
            raise ValueError("Invalid value for `note`, must not be `None`")  # noqa: E501
        self._note = note

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
        if not isinstance(other, MarkdownViewProperties):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return true if both objects are not equal."""
        return not self == other
