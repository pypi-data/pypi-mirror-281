# coding: utf-8

"""
InfluxDB OSS API Service.

The InfluxDB v2 API provides a programmatic interface for all interactions with InfluxDB. Access the InfluxDB API using the `/api/v2/` endpoint.   # noqa: E501

OpenAPI spec version: 2.0.0
Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401


class TableViewPropertiesTableOptions(object):
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
        'vertical_time_axis': 'bool',
        'sort_by': 'RenamableField',
        'wrapping': 'str',
        'fix_first_column': 'bool'
    }

    attribute_map = {
        'vertical_time_axis': 'verticalTimeAxis',
        'sort_by': 'sortBy',
        'wrapping': 'wrapping',
        'fix_first_column': 'fixFirstColumn'
    }

    def __init__(self, vertical_time_axis=None, sort_by=None, wrapping=None, fix_first_column=None):  # noqa: E501,D401,D403
        """TableViewPropertiesTableOptions - a model defined in OpenAPI."""  # noqa: E501
        self._vertical_time_axis = None
        self._sort_by = None
        self._wrapping = None
        self._fix_first_column = None
        self.discriminator = None

        if vertical_time_axis is not None:
            self.vertical_time_axis = vertical_time_axis
        if sort_by is not None:
            self.sort_by = sort_by
        if wrapping is not None:
            self.wrapping = wrapping
        if fix_first_column is not None:
            self.fix_first_column = fix_first_column

    @property
    def vertical_time_axis(self):
        """Get the vertical_time_axis of this TableViewPropertiesTableOptions.

        verticalTimeAxis describes the orientation of the table by indicating whether the time axis will be displayed vertically

        :return: The vertical_time_axis of this TableViewPropertiesTableOptions.
        :rtype: bool
        """  # noqa: E501
        return self._vertical_time_axis

    @vertical_time_axis.setter
    def vertical_time_axis(self, vertical_time_axis):
        """Set the vertical_time_axis of this TableViewPropertiesTableOptions.

        verticalTimeAxis describes the orientation of the table by indicating whether the time axis will be displayed vertically

        :param vertical_time_axis: The vertical_time_axis of this TableViewPropertiesTableOptions.
        :type: bool
        """  # noqa: E501
        self._vertical_time_axis = vertical_time_axis

    @property
    def sort_by(self):
        """Get the sort_by of this TableViewPropertiesTableOptions.

        :return: The sort_by of this TableViewPropertiesTableOptions.
        :rtype: RenamableField
        """  # noqa: E501
        return self._sort_by

    @sort_by.setter
    def sort_by(self, sort_by):
        """Set the sort_by of this TableViewPropertiesTableOptions.

        :param sort_by: The sort_by of this TableViewPropertiesTableOptions.
        :type: RenamableField
        """  # noqa: E501
        self._sort_by = sort_by

    @property
    def wrapping(self):
        """Get the wrapping of this TableViewPropertiesTableOptions.

        Wrapping describes the text wrapping style to be used in table views

        :return: The wrapping of this TableViewPropertiesTableOptions.
        :rtype: str
        """  # noqa: E501
        return self._wrapping

    @wrapping.setter
    def wrapping(self, wrapping):
        """Set the wrapping of this TableViewPropertiesTableOptions.

        Wrapping describes the text wrapping style to be used in table views

        :param wrapping: The wrapping of this TableViewPropertiesTableOptions.
        :type: str
        """  # noqa: E501
        self._wrapping = wrapping

    @property
    def fix_first_column(self):
        """Get the fix_first_column of this TableViewPropertiesTableOptions.

        fixFirstColumn indicates whether the first column of the table should be locked

        :return: The fix_first_column of this TableViewPropertiesTableOptions.
        :rtype: bool
        """  # noqa: E501
        return self._fix_first_column

    @fix_first_column.setter
    def fix_first_column(self, fix_first_column):
        """Set the fix_first_column of this TableViewPropertiesTableOptions.

        fixFirstColumn indicates whether the first column of the table should be locked

        :param fix_first_column: The fix_first_column of this TableViewPropertiesTableOptions.
        :type: bool
        """  # noqa: E501
        self._fix_first_column = fix_first_column

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
        if not isinstance(other, TableViewPropertiesTableOptions):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return true if both objects are not equal."""
        return not self == other
