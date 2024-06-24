# coding: utf-8

"""
InfluxDB OSS API Service.

The InfluxDB v2 API provides a programmatic interface for all interactions with InfluxDB. Access the InfluxDB API using the `/api/v2/` endpoint.   # noqa: E501

OpenAPI spec version: 2.0.0
Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401


class OnboardingRequest(object):
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
        'username': 'str',
        'password': 'str',
        'org': 'str',
        'bucket': 'str',
        'retention_period_seconds': 'int',
        'retention_period_hrs': 'int',
        'token': 'str'
    }

    attribute_map = {
        'username': 'username',
        'password': 'password',
        'org': 'org',
        'bucket': 'bucket',
        'retention_period_seconds': 'retentionPeriodSeconds',
        'retention_period_hrs': 'retentionPeriodHrs',
        'token': 'token'
    }

    def __init__(self, username=None, password=None, org=None, bucket=None, retention_period_seconds=None, retention_period_hrs=None, token=None):  # noqa: E501,D401,D403
        """OnboardingRequest - a model defined in OpenAPI."""  # noqa: E501
        self._username = None
        self._password = None
        self._org = None
        self._bucket = None
        self._retention_period_seconds = None
        self._retention_period_hrs = None
        self._token = None
        self.discriminator = None

        self.username = username
        if password is not None:
            self.password = password
        self.org = org
        self.bucket = bucket
        if retention_period_seconds is not None:
            self.retention_period_seconds = retention_period_seconds
        if retention_period_hrs is not None:
            self.retention_period_hrs = retention_period_hrs
        if token is not None:
            self.token = token

    @property
    def username(self):
        """Get the username of this OnboardingRequest.

        :return: The username of this OnboardingRequest.
        :rtype: str
        """  # noqa: E501
        return self._username

    @username.setter
    def username(self, username):
        """Set the username of this OnboardingRequest.

        :param username: The username of this OnboardingRequest.
        :type: str
        """  # noqa: E501
        if username is None:
            raise ValueError("Invalid value for `username`, must not be `None`")  # noqa: E501
        self._username = username

    @property
    def password(self):
        """Get the password of this OnboardingRequest.

        :return: The password of this OnboardingRequest.
        :rtype: str
        """  # noqa: E501
        return self._password

    @password.setter
    def password(self, password):
        """Set the password of this OnboardingRequest.

        :param password: The password of this OnboardingRequest.
        :type: str
        """  # noqa: E501
        self._password = password

    @property
    def org(self):
        """Get the org of this OnboardingRequest.

        :return: The org of this OnboardingRequest.
        :rtype: str
        """  # noqa: E501
        return self._org

    @org.setter
    def org(self, org):
        """Set the org of this OnboardingRequest.

        :param org: The org of this OnboardingRequest.
        :type: str
        """  # noqa: E501
        if org is None:
            raise ValueError("Invalid value for `org`, must not be `None`")  # noqa: E501
        self._org = org

    @property
    def bucket(self):
        """Get the bucket of this OnboardingRequest.

        :return: The bucket of this OnboardingRequest.
        :rtype: str
        """  # noqa: E501
        return self._bucket

    @bucket.setter
    def bucket(self, bucket):
        """Set the bucket of this OnboardingRequest.

        :param bucket: The bucket of this OnboardingRequest.
        :type: str
        """  # noqa: E501
        if bucket is None:
            raise ValueError("Invalid value for `bucket`, must not be `None`")  # noqa: E501
        self._bucket = bucket

    @property
    def retention_period_seconds(self):
        """Get the retention_period_seconds of this OnboardingRequest.

        :return: The retention_period_seconds of this OnboardingRequest.
        :rtype: int
        """  # noqa: E501
        return self._retention_period_seconds

    @retention_period_seconds.setter
    def retention_period_seconds(self, retention_period_seconds):
        """Set the retention_period_seconds of this OnboardingRequest.

        :param retention_period_seconds: The retention_period_seconds of this OnboardingRequest.
        :type: int
        """  # noqa: E501
        self._retention_period_seconds = retention_period_seconds

    @property
    def retention_period_hrs(self):
        """Get the retention_period_hrs of this OnboardingRequest.

        Retention period *in nanoseconds* for the new bucket. This key's name has been misleading since OSS 2.0 GA, please transition to use `retentionPeriodSeconds`

        :return: The retention_period_hrs of this OnboardingRequest.
        :rtype: int
        """  # noqa: E501
        return self._retention_period_hrs

    @retention_period_hrs.setter
    def retention_period_hrs(self, retention_period_hrs):
        """Set the retention_period_hrs of this OnboardingRequest.

        Retention period *in nanoseconds* for the new bucket. This key's name has been misleading since OSS 2.0 GA, please transition to use `retentionPeriodSeconds`

        :param retention_period_hrs: The retention_period_hrs of this OnboardingRequest.
        :type: int
        """  # noqa: E501
        self._retention_period_hrs = retention_period_hrs

    @property
    def token(self):
        """Get the token of this OnboardingRequest.

        Authentication token to set on the initial user. If not specified, the server will generate a token.

        :return: The token of this OnboardingRequest.
        :rtype: str
        """  # noqa: E501
        return self._token

    @token.setter
    def token(self, token):
        """Set the token of this OnboardingRequest.

        Authentication token to set on the initial user. If not specified, the server will generate a token.

        :param token: The token of this OnboardingRequest.
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
        if not isinstance(other, OnboardingRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return true if both objects are not equal."""
        return not self == other
