# coding: utf-8

"""
InfluxDB OSS API Service.

The InfluxDB v2 API provides a programmatic interface for all interactions with InfluxDB. Access the InfluxDB API using the `/api/v2/` endpoint.   # noqa: E501

OpenAPI spec version: 2.0.0
Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401


class Source(object):
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
        'links': 'SourceLinks',
        'id': 'str',
        'org_id': 'str',
        'default': 'bool',
        'name': 'str',
        'type': 'str',
        'url': 'str',
        'insecure_skip_verify': 'bool',
        'telegraf': 'str',
        'token': 'str',
        'username': 'str',
        'password': 'str',
        'shared_secret': 'str',
        'meta_url': 'str',
        'default_rp': 'str',
        'languages': 'list[str]'
    }

    attribute_map = {
        'links': 'links',
        'id': 'id',
        'org_id': 'orgID',
        'default': 'default',
        'name': 'name',
        'type': 'type',
        'url': 'url',
        'insecure_skip_verify': 'insecureSkipVerify',
        'telegraf': 'telegraf',
        'token': 'token',
        'username': 'username',
        'password': 'password',
        'shared_secret': 'sharedSecret',
        'meta_url': 'metaUrl',
        'default_rp': 'defaultRP',
        'languages': 'languages'
    }

    def __init__(self, links=None, id=None, org_id=None, default=None, name=None, type=None, url=None, insecure_skip_verify=None, telegraf=None, token=None, username=None, password=None, shared_secret=None, meta_url=None, default_rp=None, languages=None):  # noqa: E501,D401,D403
        """Source - a model defined in OpenAPI."""  # noqa: E501
        self._links = None
        self._id = None
        self._org_id = None
        self._default = None
        self._name = None
        self._type = None
        self._url = None
        self._insecure_skip_verify = None
        self._telegraf = None
        self._token = None
        self._username = None
        self._password = None
        self._shared_secret = None
        self._meta_url = None
        self._default_rp = None
        self._languages = None
        self.discriminator = None

        if links is not None:
            self.links = links
        if id is not None:
            self.id = id
        if org_id is not None:
            self.org_id = org_id
        if default is not None:
            self.default = default
        if name is not None:
            self.name = name
        if type is not None:
            self.type = type
        if url is not None:
            self.url = url
        if insecure_skip_verify is not None:
            self.insecure_skip_verify = insecure_skip_verify
        if telegraf is not None:
            self.telegraf = telegraf
        if token is not None:
            self.token = token
        if username is not None:
            self.username = username
        if password is not None:
            self.password = password
        if shared_secret is not None:
            self.shared_secret = shared_secret
        if meta_url is not None:
            self.meta_url = meta_url
        if default_rp is not None:
            self.default_rp = default_rp
        if languages is not None:
            self.languages = languages

    @property
    def links(self):
        """Get the links of this Source.

        :return: The links of this Source.
        :rtype: SourceLinks
        """  # noqa: E501
        return self._links

    @links.setter
    def links(self, links):
        """Set the links of this Source.

        :param links: The links of this Source.
        :type: SourceLinks
        """  # noqa: E501
        self._links = links

    @property
    def id(self):
        """Get the id of this Source.

        :return: The id of this Source.
        :rtype: str
        """  # noqa: E501
        return self._id

    @id.setter
    def id(self, id):
        """Set the id of this Source.

        :param id: The id of this Source.
        :type: str
        """  # noqa: E501
        self._id = id

    @property
    def org_id(self):
        """Get the org_id of this Source.

        :return: The org_id of this Source.
        :rtype: str
        """  # noqa: E501
        return self._org_id

    @org_id.setter
    def org_id(self, org_id):
        """Set the org_id of this Source.

        :param org_id: The org_id of this Source.
        :type: str
        """  # noqa: E501
        self._org_id = org_id

    @property
    def default(self):
        """Get the default of this Source.

        :return: The default of this Source.
        :rtype: bool
        """  # noqa: E501
        return self._default

    @default.setter
    def default(self, default):
        """Set the default of this Source.

        :param default: The default of this Source.
        :type: bool
        """  # noqa: E501
        self._default = default

    @property
    def name(self):
        """Get the name of this Source.

        :return: The name of this Source.
        :rtype: str
        """  # noqa: E501
        return self._name

    @name.setter
    def name(self, name):
        """Set the name of this Source.

        :param name: The name of this Source.
        :type: str
        """  # noqa: E501
        self._name = name

    @property
    def type(self):
        """Get the type of this Source.

        :return: The type of this Source.
        :rtype: str
        """  # noqa: E501
        return self._type

    @type.setter
    def type(self, type):
        """Set the type of this Source.

        :param type: The type of this Source.
        :type: str
        """  # noqa: E501
        self._type = type

    @property
    def url(self):
        """Get the url of this Source.

        :return: The url of this Source.
        :rtype: str
        """  # noqa: E501
        return self._url

    @url.setter
    def url(self, url):
        """Set the url of this Source.

        :param url: The url of this Source.
        :type: str
        """  # noqa: E501
        self._url = url

    @property
    def insecure_skip_verify(self):
        """Get the insecure_skip_verify of this Source.

        :return: The insecure_skip_verify of this Source.
        :rtype: bool
        """  # noqa: E501
        return self._insecure_skip_verify

    @insecure_skip_verify.setter
    def insecure_skip_verify(self, insecure_skip_verify):
        """Set the insecure_skip_verify of this Source.

        :param insecure_skip_verify: The insecure_skip_verify of this Source.
        :type: bool
        """  # noqa: E501
        self._insecure_skip_verify = insecure_skip_verify

    @property
    def telegraf(self):
        """Get the telegraf of this Source.

        :return: The telegraf of this Source.
        :rtype: str
        """  # noqa: E501
        return self._telegraf

    @telegraf.setter
    def telegraf(self, telegraf):
        """Set the telegraf of this Source.

        :param telegraf: The telegraf of this Source.
        :type: str
        """  # noqa: E501
        self._telegraf = telegraf

    @property
    def token(self):
        """Get the token of this Source.

        :return: The token of this Source.
        :rtype: str
        """  # noqa: E501
        return self._token

    @token.setter
    def token(self, token):
        """Set the token of this Source.

        :param token: The token of this Source.
        :type: str
        """  # noqa: E501
        self._token = token

    @property
    def username(self):
        """Get the username of this Source.

        :return: The username of this Source.
        :rtype: str
        """  # noqa: E501
        return self._username

    @username.setter
    def username(self, username):
        """Set the username of this Source.

        :param username: The username of this Source.
        :type: str
        """  # noqa: E501
        self._username = username

    @property
    def password(self):
        """Get the password of this Source.

        :return: The password of this Source.
        :rtype: str
        """  # noqa: E501
        return self._password

    @password.setter
    def password(self, password):
        """Set the password of this Source.

        :param password: The password of this Source.
        :type: str
        """  # noqa: E501
        self._password = password

    @property
    def shared_secret(self):
        """Get the shared_secret of this Source.

        :return: The shared_secret of this Source.
        :rtype: str
        """  # noqa: E501
        return self._shared_secret

    @shared_secret.setter
    def shared_secret(self, shared_secret):
        """Set the shared_secret of this Source.

        :param shared_secret: The shared_secret of this Source.
        :type: str
        """  # noqa: E501
        self._shared_secret = shared_secret

    @property
    def meta_url(self):
        """Get the meta_url of this Source.

        :return: The meta_url of this Source.
        :rtype: str
        """  # noqa: E501
        return self._meta_url

    @meta_url.setter
    def meta_url(self, meta_url):
        """Set the meta_url of this Source.

        :param meta_url: The meta_url of this Source.
        :type: str
        """  # noqa: E501
        self._meta_url = meta_url

    @property
    def default_rp(self):
        """Get the default_rp of this Source.

        :return: The default_rp of this Source.
        :rtype: str
        """  # noqa: E501
        return self._default_rp

    @default_rp.setter
    def default_rp(self, default_rp):
        """Set the default_rp of this Source.

        :param default_rp: The default_rp of this Source.
        :type: str
        """  # noqa: E501
        self._default_rp = default_rp

    @property
    def languages(self):
        """Get the languages of this Source.

        :return: The languages of this Source.
        :rtype: list[str]
        """  # noqa: E501
        return self._languages

    @languages.setter
    def languages(self, languages):
        """Set the languages of this Source.

        :param languages: The languages of this Source.
        :type: list[str]
        """  # noqa: E501
        allowed_values = ["flux", "influxql"]  # noqa: E501
        if not set(languages).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values for `languages` [{0}], must be a subset of [{1}]"  # noqa: E501
                .format(", ".join(map(str, set(languages) - set(allowed_values))),  # noqa: E501
                        ", ".join(map(str, allowed_values)))
            )
        self._languages = languages

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
        if not isinstance(other, Source):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Return true if both objects are not equal."""
        return not self == other
