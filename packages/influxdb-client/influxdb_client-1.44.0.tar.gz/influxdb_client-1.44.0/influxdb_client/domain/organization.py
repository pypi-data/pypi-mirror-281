# coding: utf-8

"""
InfluxDB OSS API Service.

The InfluxDB v2 API provides a programmatic interface for all interactions with InfluxDB. Access the InfluxDB API using the `/api/v2/` endpoint.   # noqa: E501

OpenAPI spec version: 2.0.0
Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401


class Organization(object):
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
        'links': 'OrganizationLinks',
        'id': 'str',
        'name': 'str',
        'default_storage_type': 'str',
        'description': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'status': 'str'
    }

    attribute_map = {
        'links': 'links',
        'id': 'id',
        'name': 'name',
        'default_storage_type': 'defaultStorageType',
        'description': 'description',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'status': 'status'
    }

    def __init__(self, links=None, id=None, name=None, default_storage_type=None, description=None, created_at=None, updated_at=None, status='active'):  # noqa: E501,D401,D403
        """Organization - a model defined in OpenAPI."""  # noqa: E501
        self._links = None
        self._id = None
        self._name = None
        self._default_storage_type = None
        self._description = None
        self._created_at = None
        self._updated_at = None
        self._status = None
        self.discriminator = None

        if links is not None:
            self.links = links
        if id is not None:
            self.id = id
        self.name = name
        if default_storage_type is not None:
            self.default_storage_type = default_storage_type
        if description is not None:
            self.description = description
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if status is not None:
            self.status = status

    @property
    def links(self):
        """Get the links of this Organization.

        :return: The links of this Organization.
        :rtype: OrganizationLinks
        """  # noqa: E501
        return self._links

    @links.setter
    def links(self, links):
        """Set the links of this Organization.

        :param links: The links of this Organization.
        :type: OrganizationLinks
        """  # noqa: E501
        self._links = links

    @property
    def id(self):
        """Get the id of this Organization.

        :return: The id of this Organization.
        :rtype: str
        """  # noqa: E501
        return self._id

    @id.setter
    def id(self, id):
        """Set the id of this Organization.

        :param id: The id of this Organization.
        :type: str
        """  # noqa: E501
        self._id = id

    @property
    def name(self):
        """Get the name of this Organization.

        :return: The name of this Organization.
        :rtype: str
        """  # noqa: E501
        return self._name

    @name.setter
    def name(self, name):
        """Set the name of this Organization.

        :param name: The name of this Organization.
        :type: str
        """  # noqa: E501
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        self._name = name

    @property
    def default_storage_type(self):
        """Get the default_storage_type of this Organization.

        Discloses whether the organization uses TSM or IOx.

        :return: The default_storage_type of this Organization.
        :rtype: str
        """  # noqa: E501
        return self._default_storage_type

    @default_storage_type.setter
    def default_storage_type(self, default_storage_type):
        """Set the default_storage_type of this Organization.

        Discloses whether the organization uses TSM or IOx.

        :param default_storage_type: The default_storage_type of this Organization.
        :type: str
        """  # noqa: E501
        self._default_storage_type = default_storage_type

    @property
    def description(self):
        """Get the description of this Organization.

        :return: The description of this Organization.
        :rtype: str
        """  # noqa: E501
        return self._description

    @description.setter
    def description(self, description):
        """Set the description of this Organization.

        :param description: The description of this Organization.
        :type: str
        """  # noqa: E501
        self._description = description

    @property
    def created_at(self):
        """Get the created_at of this Organization.

        :return: The created_at of this Organization.
        :rtype: datetime
        """  # noqa: E501
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Set the created_at of this Organization.

        :param created_at: The created_at of this Organization.
        :type: datetime
        """  # noqa: E501
        self._created_at = created_at

    @property
    def updated_at(self):
        """Get the updated_at of this Organization.

        :return: The updated_at of this Organization.
        :rtype: datetime
        """  # noqa: E501
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Set the updated_at of this Organization.

        :param updated_at: The updated_at of this Organization.
        :type: datetime
        """  # noqa: E501
        self._updated_at = updated_at

    @property
    def status(self):
        """Get the status of this Organization.

        If inactive, the organization is inactive.

        :return: The status of this Organization.
        :rtype: str
        """  # noqa: E501
        return self._status

    @status.setter
    def status(self, status):
        """Set the status of this Organization.

        If inactive, the organization is inactive.

        :param status: The status of this Organization.
        :type: str
        """  # noqa: E501
        self._status = status

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
        if not isinstance(other, Organization):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return true if both objects are not equal."""
        return not self == other
