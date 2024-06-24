# coding: utf-8

"""
InfluxDB OSS API Service.

The InfluxDB v2 API provides a programmatic interface for all interactions with InfluxDB. Access the InfluxDB API using the `/api/v2/` endpoint.   # noqa: E501

OpenAPI spec version: 2.0.0
Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

from influxdb_client.domain.notification_endpoint_discriminator import NotificationEndpointDiscriminator


class SlackNotificationEndpoint(NotificationEndpointDiscriminator):
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
        'url': 'str',
        'token': 'str',
        'id': 'str',
        'org_id': 'str',
        'user_id': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'description': 'str',
        'name': 'str',
        'status': 'str',
        'labels': 'list[Label]',
        'links': 'NotificationEndpointBaseLinks',
        'type': 'NotificationEndpointType'
    }

    attribute_map = {
        'url': 'url',
        'token': 'token',
        'id': 'id',
        'org_id': 'orgID',
        'user_id': 'userID',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'description': 'description',
        'name': 'name',
        'status': 'status',
        'labels': 'labels',
        'links': 'links',
        'type': 'type'
    }

    def __init__(self, url=None, token=None, id=None, org_id=None, user_id=None, created_at=None, updated_at=None, description=None, name=None, status='active', labels=None, links=None, type="slack"):  # noqa: E501,D401,D403
        """SlackNotificationEndpoint - a model defined in OpenAPI."""  # noqa: E501
        NotificationEndpointDiscriminator.__init__(self, id=id, org_id=org_id, user_id=user_id, created_at=created_at, updated_at=updated_at, description=description, name=name, status=status, labels=labels, links=links, type=type)  # noqa: E501

        self._url = None
        self._token = None
        self.discriminator = None

        if url is not None:
            self.url = url
        if token is not None:
            self.token = token

    @property
    def url(self):
        """Get the url of this SlackNotificationEndpoint.

        Specifies the URL of the Slack endpoint. Specify either `URL` or `Token`.

        :return: The url of this SlackNotificationEndpoint.
        :rtype: str
        """  # noqa: E501
        return self._url

    @url.setter
    def url(self, url):
        """Set the url of this SlackNotificationEndpoint.

        Specifies the URL of the Slack endpoint. Specify either `URL` or `Token`.

        :param url: The url of this SlackNotificationEndpoint.
        :type: str
        """  # noqa: E501
        self._url = url

    @property
    def token(self):
        """Get the token of this SlackNotificationEndpoint.

        Specifies the API token string. Specify either `URL` or `Token`.

        :return: The token of this SlackNotificationEndpoint.
        :rtype: str
        """  # noqa: E501
        return self._token

    @token.setter
    def token(self, token):
        """Set the token of this SlackNotificationEndpoint.

        Specifies the API token string. Specify either `URL` or `Token`.

        :param token: The token of this SlackNotificationEndpoint.
        :type: str
        """  # noqa: E501
        self._token = token

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
        if not isinstance(other, SlackNotificationEndpoint):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return true if both objects are not equal."""
        return not self == other
