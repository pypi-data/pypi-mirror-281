# coding: utf-8

"""
InfluxDB OSS API Service.

The InfluxDB v2 API provides a programmatic interface for all interactions with InfluxDB. Access the InfluxDB API using the `/api/v2/` endpoint.   # noqa: E501

OpenAPI spec version: 2.0.0
Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401


class LabelMapping(object):
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
        'label_id': 'str'
    }

    attribute_map = {
        'label_id': 'labelID'
    }

    def __init__(self, label_id=None):  # noqa: E501,D401,D403
        """LabelMapping - a model defined in OpenAPI."""  # noqa: E501
        self._label_id = None
        self.discriminator = None

        self.label_id = label_id

    @property
    def label_id(self):
        """Get the label_id of this LabelMapping.

        A label ID. Specifies the label to attach.

        :return: The label_id of this LabelMapping.
        :rtype: str
        """  # noqa: E501
        return self._label_id

    @label_id.setter
    def label_id(self, label_id):
        """Set the label_id of this LabelMapping.

        A label ID. Specifies the label to attach.

        :param label_id: The label_id of this LabelMapping.
        :type: str
        """  # noqa: E501
        if label_id is None:
            raise ValueError("Invalid value for `label_id`, must not be `None`")  # noqa: E501
        self._label_id = label_id

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
        if not isinstance(other, LabelMapping):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return true if both objects are not equal."""
        return not self == other
