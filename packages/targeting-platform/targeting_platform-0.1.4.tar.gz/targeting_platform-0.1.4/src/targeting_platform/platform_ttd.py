"""The Trade Desk (TTD) API Integration."""

from typing import Any, Dict, List, cast
from typing_extensions import override
from targeting_platform.platform import Platform


class PlatformTTD(Platform):
    """Implementation of The Trade Desk (TDD) Activation Platfrom."""

    CHANNELS_MAPPING: Dict[str, str] = {
        "Other": "Display",
        "Display": "Display",
        "Video": "Video",
        "Audio": "Audio",
        "Native": "Display",
        "NativeDisplay": "Display",
        "NativeVideo": "Video",
        "TV": "Connected TV",
        "TVPersonal": "Connected TV",
        "OutOfHome": "DOOH",
        "Mixed": "Display",
    }
    _MAX_LOCATION_PER_PLACEMENT: int = 10000
    _MAX_LOCATION_RADIUS: int = 100000  # km
    _CHUNK_SIZE: int = 10000
    _CACHE_TTL: int = 86400  # Seconds

    @override
    def _set_credentials(self, credentials: Any) -> None:
        """Set platfrom credentials.

        Args:
        ----
            credentials (Any): Provided credentials. Format: {"api_url":"","partner_id":"","token":"","login":"","password":""}.

        """
        self._credentials: Dict[str, Any] = credentials
        self._api_headers = {
            "Content-Type": "application/json",
            "TTD-Auth": self._credentials.get("token", ""),
        }
        self._API_URL = self._credentials.get("api_url", "")

    @override
    def _is_credentials(self) -> bool:
        """Check if credential is valid and reissue token if needed.

        Returns
        -------
            bool: if can connect.

        """
        if not self._API_URL or not self._credentials.get("token", ""):
            return False
        response = self._http_session.post(
            f"{self._API_URL}introspectToken",
            headers=self._api_headers,
            timeout=None,
        )
        if response.status_code != 200:
            # Get new token
            if self._credentials:
                response = self._http_session.post(
                    f"{self._API_URL}authentication",
                    json={
                        "Login": self._credentials.get("login", ""),
                        "Password": self._credentials.get("password", ""),
                        "TokenExpirationInMinutes": 1440,
                    },
                    timeout=None,
                )
                if response.status_code == 200:
                    self._api_headers = {
                        "Content-Type": "application/json",
                        "TTD-Auth": response.json().get("Token", ""),
                    }
                else:
                    raise Exception(response.text)
            else:
                return False
        return True

    def _get_advertizer(self, advertizer_id: str, is_force_update: bool = False) -> Dict[str, Any]:
        """Get advertiser information from platform.

        Args:
        ----
            advertizer_id (str): advertizer_id.
            is_force_update (bool): force to update from API even if already in cache.

        Returns:
        -------
            Dict[str, Any]: Advertiser information.

        """
        partner_id = self._credentials.get("partner_id", "")
        cached_values: Dict[str, Any] | None = None if is_force_update else self._cache.get_cache(name="ttd_advertiser", partner_id=partner_id)
        if (cached_values is None or is_force_update) and self._is_credentials():
            response = self._http_session.post(
                f"{self._API_URL}delta/advertiser/query/partner",
                headers=self._api_headers,
                json={
                    "PartnerId": partner_id,
                    "ReturnEntireAdvertiser": True,
                    "LastChangeTrackingVersion": cached_values.get("LastChangeTrackingVersion", None) if cached_values else None,
                },
                timeout=None,
            )
            response.raise_for_status()

            result = response.json()
            if result.get("Advertisers", []):
                # There is new data
                new_advertisers = {advertiser["AdvertiserId"]: advertiser for advertiser in result.get("Advertisers", [])}
                if cached_values:
                    cached_values["Advertisers"].update(new_advertisers)
                    cached_values["LastChangeTrackingVersion"] = result["LastChangeTrackingVersion"]
                else:
                    cached_values = {
                        "Advertisers": new_advertisers,
                        "LastChangeTrackingVersion": result["LastChangeTrackingVersion"],
                    }
            self._cache.set_cache(
                name="ttd_advertiser",
                value=cached_values,
                ttl=self._CACHE_TTL,
                partner_id=partner_id,
            )
        return cast(Dict[str, Any], cached_values.get("Advertisers", {}).get(advertizer_id, {})) if cached_values else {}

    def _get_advertiser_campaigns(self, advertizer_id: str, is_force_update: bool = False) -> Dict[str, Any]:
        """Get Campaigns information from platform.

        Args:
        ----
            advertizer_id (str): advertizer_id.
            is_force_update (bool): force to update from API even if already in cache.


        Returns:
        -------
            Dict[str, Any]: Campaigns information.

        """
        cached_values: Dict[str, Any] | None = None if is_force_update else self._cache.get_cache(name="ttd_advertiser_campaigns", advertizer_id=advertizer_id)
        if (cached_values is None or is_force_update) and self._is_credentials():
            response = self._http_session.post(
                f"{self._API_URL}delta/campaign/query/advertiser",
                headers=self._api_headers,
                json={
                    "AdvertiserId": advertizer_id,
                    "ReturnEntireCampaign": True,
                    "LastChangeTrackingVersion": cached_values.get("LastChangeTrackingVersion", None) if cached_values else None,
                },
                timeout=None,
            )
            response.raise_for_status()

            result = response.json()
            if result.get("Campaigns", []):
                # There is new data
                new_campaigns = {campaign["CampaignId"]: campaign for campaign in result.get("Campaigns", [])}
                if cached_values:
                    cached_values["Campaigns"].update(new_campaigns)
                    cached_values["LastChangeTrackingVersion"] = result["LastChangeTrackingVersion"]
                else:
                    cached_values = {
                        "Campaigns": new_campaigns,
                        "LastChangeTrackingVersion": result["LastChangeTrackingVersion"],
                    }

            self._cache.set_cache(
                name="ttd_advertiser_campaigns",
                value=cached_values,
                ttl=self._CACHE_TTL,
                advertizer_id=advertizer_id,
            )

        return cast(Dict[str, Any], cached_values.get("Campaigns", {})) if cached_values else {}

    def _get_advertiser_adgroups(self, advertizer_id: str, is_force_update: bool = False) -> Dict[str, Any]:
        """Get AdGroups information from platform.

        Args:
        ----
            advertizer_id (str): advertizer_id.
            is_force_update (bool): force to update from API even if already in cache.


        Returns:
        -------
            Dict[str, Any]: AdGroups information.

        """
        cached_values: Dict[str, Any] | None = None if is_force_update else self._cache.get_cache(name="ttd_advertiser_adgroups", advertizer_id=advertizer_id)
        if (cached_values is None or is_force_update) and self._is_credentials():
            response = self._http_session.post(
                f"{self._API_URL}delta/adgroup/query/advertiser",
                headers=self._api_headers,
                json={
                    "AdvertiserId": advertizer_id,
                    "ReturnEntireAdGroup": True,
                    "IncludeTemplates": False,
                    "LastChangeTrackingVersion": cached_values.get("LastChangeTrackingVersion", None) if cached_values else None,
                },
                timeout=None,
            )
            response.raise_for_status()

            result = response.json()
            if result.get("AdGroups", []):
                # There is new data
                new_adgroups = {adgroup["AdGroupId"]: adgroup for adgroup in result.get("AdGroups", [])}
                if cached_values:
                    cached_values["AdGroups"].update(new_adgroups)
                    cached_values["LastChangeTrackingVersion"] = result["LastChangeTrackingVersion"]
                else:
                    cached_values = {
                        "AdGroups": new_adgroups,
                        "LastChangeTrackingVersion": result["LastChangeTrackingVersion"],
                    }

            self._cache.set_cache(
                name="ttd_advertiser_adgroups",
                value=cached_values,
                ttl=self._CACHE_TTL,
                advertizer_id=advertizer_id,
            )

        return cast(Dict[str, Any], cached_values.get("AdGroups", {})) if cached_values else {}

    def _get_adgroup_budget(self, adgroup: Dict[str, Any]) -> float:
        """Get AdGroup budget value.

        Args:
        ----
            adgroup (Dict[str, Any]): adgroup information.

        Returns:
        -------
            float: budget value, 0 if not set.

        """
        return float(adgroup.get("RTBAttributes", {}).get("BudgetSettings", {}).get("Budget", {}).get("Amount", 0))

    @override
    def validate_credentials(self, first_level_id: str) -> bool:
        """Validate connection to the platform.

        For connection credentials from object will be used.

        Args:
        ----
            first_level_id (str): id for main platfrom identificator to validate access to.

        Returns:
        -------
            bool: True if platform can be access with current credentials and id

        """
        advertizer = self._get_advertizer(advertizer_id=first_level_id, is_force_update=True)
        return bool(advertizer)

    @override
    def get_catalog(
        self,
        first_level_id: str,
        second_level_ids: List[str] | None = None,
        only_placements: bool = False,
        no_placements: bool = False,
        is_force_update: bool = False,
    ) -> Dict[str, Any]:
        """Return catalog of elements for platfrom.

        Args:
        ----
            first_level_id (str): iadvertiser id.
            second_level_ids (List[str] | None, optional): list of campaign ids. Defaults to None.
            only_placements (bool, optional): Return only placement in response. Defaults to False.
            no_placements (bool, optional): Does not return placements in response. Defaults to False.
            is_force_update (bool, optional): Force update even if cache is exists. Defaults to False.

        Returns:
        -------
            Dict[str, Any]: platfrom catalog. Structure {"second_level_items":[{"third_level_items":[{"placements":[]}]}]}.

        """
        response: Dict[str, Any] = {}

        advertizer = self._get_advertizer(advertizer_id=first_level_id, is_force_update=is_force_update)
        adgroups = self._get_advertiser_adgroups(advertizer_id=first_level_id, is_force_update=is_force_update) if not no_placements else {}

        currency = advertizer.get("CurrencyCode", "")

        if only_placements:
            response = {
                "placements": {
                    item["AdGroupId"]: {
                        "id": item["AdGroupId"],
                        "name": item["AdGroupName"],
                        "status": "Enabled" if item["IsEnabled"] else "Disabled",
                        "budget": f"{currency} {self._get_adgroup_budget(item):.2f}",
                        "channel": self.CHANNELS_MAPPING.get(item["ChannelId"], item["ChannelId"]),
                        "start_date": "",
                        "end_date": "",
                    }
                    for item in adgroups.values()
                    if (not second_level_ids or item["CampaignId"] in second_level_ids) and item["Availability"] != "Archived"
                }
            }
        else:
            campaigns_dict: Dict[str, List[Dict[str, Any]]] = {}
            for item in adgroups.values():
                if (not second_level_ids or item["CampaignId"] in second_level_ids) and item["Availability"] != "Archived":
                    if item["CampaignId"] not in campaigns_dict:
                        campaigns_dict[item["CampaignId"]] = []
                    campaigns_dict[item["CampaignId"]].append(
                        {
                            "id": item["AdGroupId"],
                            "name": item["AdGroupName"],
                            "status": "Enabled" if item["IsEnabled"] else "Disabled",
                            "budget": f"{currency} {self._get_adgroup_budget(item):.2f}",
                            "channel": self.CHANNELS_MAPPING.get(item["ChannelId"], item["ChannelId"]),
                            "is_duplicate": False,
                            "is_youtube": False,
                        }
                    )
            campaigns = self._get_advertiser_campaigns(advertizer_id=first_level_id, is_force_update=is_force_update) if not only_placements else {}
            response = {
                "second_level_items": [
                    {
                        "id": campaign["CampaignId"],
                        "name": campaign["CampaignName"],
                        "status": campaign["Availability"],
                        "start_date": campaign.get("StartDate", "")[:10],
                        "end_date": campaign.get("EndDate", "")[:10],
                        "third_level_items": [
                            {
                                "id": "",
                                "name": "",
                                "status": "",
                                "placements": [
                                    placement
                                    | {
                                        "start_date": campaign.get("StartDate", "")[:10],
                                        "end_date": campaign.get("EndDate", "")[:10],
                                    }
                                    for placement in campaigns_dict.get(campaign["CampaignId"], [])
                                ],
                            }
                        ],
                    }
                    for campaign in campaigns.values()
                    if (not second_level_ids or campaign["CampaignId"] in second_level_ids) and campaign["Availability"] != "Archived"
                ]
            }

        return response

    @override
    def get_all_placements(self, first_level_id: str, second_level_id: str | None = None, third_level_id: str | None = None) -> Dict[str, List[Dict[str, Any]]]:
        """Get all placements.

        Args:
        ----
            first_level_id (str): id for main platfrom identificator to get catalog for.
            second_level_id (str | None, optional): list of second level elements to get (campaigns e.g.). Defaults to None.
            third_level_id (str | None, optional): list of third level elements to get (insertion orders e.g.). Defaults to None.

        Returns:
        -------
            Dict[str, List[Dict[str, Any]]]: placements information.

        """
        adgroups = self._get_advertiser_adgroups(advertizer_id=first_level_id, is_force_update=True)
        return {"placements": [item for item in adgroups.values() if not second_level_id or item["CampaignId"] == second_level_id]}

    @override
    def get_placement(self, first_level_id: str, placement_id: str) -> Any:
        """Get placement.

        Args:
        ----
            first_level_id (str): id for main platfrom identificator to get catalog for.
            placement_id (str): placement id to duplicate.

        Returns:
        -------
            Any: placement object or information.

        """
        result: Dict[str, Any] = {}
        if self._is_credentials():
            response = self._http_session.get(
                f"{self._API_URL}adgroup/{placement_id}",
                headers=self._api_headers,
                timeout=None,
            )
            response.raise_for_status()
            if response.status_code == 200:
                result = response.json()
        return result

    @override
    def pause_placement(self, first_level_id: str, placement_ids: List[str]) -> List[str]:
        """Pause placement.

        Args:
        ----
            first_level_id (str): id for main platfrom identificator to get catalog for.
            placement_ids (List[str]): placement ids to pause.

        Returns:
        -------
            list: list of paused placement ids.

        """
        result: List[str] = []
        if self._is_credentials():
            for adgroup_id in placement_ids:
                response = self._http_session.put(
                    f"{self._API_URL}adgroup",
                    headers=self._api_headers,
                    json={"AdGroupId": adgroup_id, "IsEnabled": False},
                    timeout=None,
                )
                response.raise_for_status()
                if response.status_code == 200:
                    result.append(adgroup_id)

        return result
