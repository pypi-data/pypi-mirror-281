# coding: utf-8

"""
InfluxDB OSS API Service.

The InfluxDB v2 API provides a programmatic interface for all interactions with InfluxDB. Access the InfluxDB API using the `/api/v2/` endpoint.   # noqa: E501

OpenAPI spec version: 2.0.0
Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401


class TemplateExportByIDResourceFilters(object):
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
        'by_label': 'list[str]',
        'by_resource_kind': 'list[TemplateKind]'
    }

    attribute_map = {
        'by_label': 'byLabel',
        'by_resource_kind': 'byResourceKind'
    }

    def __init__(self, by_label=None, by_resource_kind=None):  # noqa: E501,D401,D403
        """TemplateExportByIDResourceFilters - a model defined in OpenAPI."""  # noqa: E501
        self._by_label = None
        self._by_resource_kind = None
        self.discriminator = None

        if by_label is not None:
            self.by_label = by_label
        if by_resource_kind is not None:
            self.by_resource_kind = by_resource_kind

    @property
    def by_label(self):
        """Get the by_label of this TemplateExportByIDResourceFilters.

        :return: The by_label of this TemplateExportByIDResourceFilters.
        :rtype: list[str]
        """  # noqa: E501
        return self._by_label

    @by_label.setter
    def by_label(self, by_label):
        """Set the by_label of this TemplateExportByIDResourceFilters.

        :param by_label: The by_label of this TemplateExportByIDResourceFilters.
        :type: list[str]
        """  # noqa: E501
        self._by_label = by_label

    @property
    def by_resource_kind(self):
        """Get the by_resource_kind of this TemplateExportByIDResourceFilters.

        :return: The by_resource_kind of this TemplateExportByIDResourceFilters.
        :rtype: list[TemplateKind]
        """  # noqa: E501
        return self._by_resource_kind

    @by_resource_kind.setter
    def by_resource_kind(self, by_resource_kind):
        """Set the by_resource_kind of this TemplateExportByIDResourceFilters.

        :param by_resource_kind: The by_resource_kind of this TemplateExportByIDResourceFilters.
        :type: list[TemplateKind]
        """  # noqa: E501
        self._by_resource_kind = by_resource_kind

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
        if not isinstance(other, TemplateExportByIDResourceFilters):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return true if both objects are not equal."""
        return not self == other
