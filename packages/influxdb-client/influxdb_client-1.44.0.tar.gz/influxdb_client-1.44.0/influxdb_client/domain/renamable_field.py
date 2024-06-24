# coding: utf-8

"""
InfluxDB OSS API Service.

The InfluxDB v2 API provides a programmatic interface for all interactions with InfluxDB. Access the InfluxDB API using the `/api/v2/` endpoint.   # noqa: E501

OpenAPI spec version: 2.0.0
Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401


class RenamableField(object):
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
        'internal_name': 'str',
        'display_name': 'str',
        'visible': 'bool'
    }

    attribute_map = {
        'internal_name': 'internalName',
        'display_name': 'displayName',
        'visible': 'visible'
    }

    def __init__(self, internal_name=None, display_name=None, visible=None):  # noqa: E501,D401,D403
        """RenamableField - a model defined in OpenAPI."""  # noqa: E501
        self._internal_name = None
        self._display_name = None
        self._visible = None
        self.discriminator = None

        if internal_name is not None:
            self.internal_name = internal_name
        if display_name is not None:
            self.display_name = display_name
        if visible is not None:
            self.visible = visible

    @property
    def internal_name(self):
        """Get the internal_name of this RenamableField.

        The calculated name of a field.

        :return: The internal_name of this RenamableField.
        :rtype: str
        """  # noqa: E501
        return self._internal_name

    @internal_name.setter
    def internal_name(self, internal_name):
        """Set the internal_name of this RenamableField.

        The calculated name of a field.

        :param internal_name: The internal_name of this RenamableField.
        :type: str
        """  # noqa: E501
        self._internal_name = internal_name

    @property
    def display_name(self):
        """Get the display_name of this RenamableField.

        The name that a field is renamed to by the user.

        :return: The display_name of this RenamableField.
        :rtype: str
        """  # noqa: E501
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Set the display_name of this RenamableField.

        The name that a field is renamed to by the user.

        :param display_name: The display_name of this RenamableField.
        :type: str
        """  # noqa: E501
        self._display_name = display_name

    @property
    def visible(self):
        """Get the visible of this RenamableField.

        Indicates whether this field should be visible on the table.

        :return: The visible of this RenamableField.
        :rtype: bool
        """  # noqa: E501
        return self._visible

    @visible.setter
    def visible(self, visible):
        """Set the visible of this RenamableField.

        Indicates whether this field should be visible on the table.

        :param visible: The visible of this RenamableField.
        :type: bool
        """  # noqa: E501
        self._visible = visible

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
        if not isinstance(other, RenamableField):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return true if both objects are not equal."""
        return not self == other
