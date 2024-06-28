import typing

from typing import Optional
from typing import List

from khulnasoft_analyze_sdk import errors
from khulnasoft_analyze_sdk._api import KhulnasoftApi
from khulnasoft_analyze_sdk.api import KhulnasoftApiClient
from khulnasoft_analyze_sdk.api import get_global_api


class Family:
    def __init__(self,
                 family_id: str,
                 name: str = None,
                 family_type: str = None,
                 *,
                 api: KhulnasoftApiClient = None):
        self.family_id = family_id
        self._name = name
        self._type = family_type
        self._tags = None
        self._api = KhulnasoftApi(api or get_global_api())

    def __eq__(self, other):
        return self is other or isinstance(other, Family) and self.family_id and other.family_id == self.family_id

    @classmethod
    def from_family_id(cls, family_id: str, api: KhulnasoftApiClient = None) -> typing.Optional['Family']:
        try:
            family = cls(family_id, api=api)
            family.fetch_info()
            return family
        except errors.FamilyNotFoundError:
            return None

    def fetch_info(self):
        info = self._api.get_family_info(self.family_id)
        if not info:
            raise errors.FamilyNotFoundError(self.family_id)

        self._name = info['family_name']
        self._type = info['family_type']
        self._tags = info.get('family_tags', [])

    @property
    def name(self) -> str:
        if not self._name:
            self.fetch_info()

        return self._name

    @property
    def type(self) -> str:
        if not self._type:
            self.fetch_info()

        return self._type

    @property
    def tags(self) -> List[str]:
        if self._tags is None:
            self.fetch_info()

        return self._tags


def get_family_by_name(family_name: str, api: KhulnasoftApiClient = None) -> typing.Optional[Family]:
    family = KhulnasoftApi(api or get_global_api()).get_family_by_name(family_name)
    if family:
        return Family(family['family_id'], family['family_name'])

    return None
