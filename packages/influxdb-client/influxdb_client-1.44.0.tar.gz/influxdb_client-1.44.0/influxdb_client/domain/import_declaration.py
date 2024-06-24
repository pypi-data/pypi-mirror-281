# coding: utf-8

"""
InfluxDB OSS API Service.

The InfluxDB v2 API provides a programmatic interface for all interactions with InfluxDB. Access the InfluxDB API using the `/api/v2/` endpoint.   # noqa: E501

OpenAPI spec version: 2.0.0
Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401


class ImportDeclaration(object):
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
        '_as': 'Identifier',
        'path': 'StringLiteral'
    }

    attribute_map = {
        'type': 'type',
        '_as': 'as',
        'path': 'path'
    }

    def __init__(self, type=None, _as=None, path=None):  # noqa: E501,D401,D403
        """ImportDeclaration - a model defined in OpenAPI."""  # noqa: E501
        self._type = None
        self.__as = None
        self._path = None
        self.discriminator = None

        if type is not None:
            self.type = type
        if _as is not None:
            self._as = _as
        if path is not None:
            self.path = path

    @property
    def type(self):
        """Get the type of this ImportDeclaration.

        Type of AST node

        :return: The type of this ImportDeclaration.
        :rtype: str
        """  # noqa: E501
        return self._type

    @type.setter
    def type(self, type):
        """Set the type of this ImportDeclaration.

        Type of AST node

        :param type: The type of this ImportDeclaration.
        :type: str
        """  # noqa: E501
        self._type = type

    @property
    def _as(self):
        """Get the _as of this ImportDeclaration.

        :return: The _as of this ImportDeclaration.
        :rtype: Identifier
        """  # noqa: E501
        return self.__as

    @_as.setter
    def _as(self, _as):
        """Set the _as of this ImportDeclaration.

        :param _as: The _as of this ImportDeclaration.
        :type: Identifier
        """  # noqa: E501
        self.__as = _as

    @property
    def path(self):
        """Get the path of this ImportDeclaration.

        :return: The path of this ImportDeclaration.
        :rtype: StringLiteral
        """  # noqa: E501
        return self._path

    @path.setter
    def path(self, path):
        """Set the path of this ImportDeclaration.

        :param path: The path of this ImportDeclaration.
        :type: StringLiteral
        """  # noqa: E501
        self._path = path

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
        if not isinstance(other, ImportDeclaration):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return true if both objects are not equal."""
        return not self == other
