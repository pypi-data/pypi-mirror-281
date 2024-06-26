"""Meta API Integration.."""

import datetime
import json
from time import sleep
from typing import Any, Dict, List, cast
import pytz
from typing_extensions import override

from targeting_platform.platform import Platform
from targeting_platform.utils_common import generate_batches
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.campaign import Campaign
from facebook_business.exceptions import FacebookRequestError


def _callback_failure(meta_response: Any) -> Any:
    raise meta_response.error()


class PlatformMeta(Platform):
    """Implementation of Meta Activation Platfrom."""

    ACCESS_ROLES = {"ADVERTISE", "MANAGE"}
    _MAX_LOCATION_PER_PLACEMENT: int = 200
    _MAX_LOCATION_RADIUS: int = 80  # km
    _CHUNK_SIZE: int = 50
    _CACHE_TTL: int = 3600  # Seconds

    _API_VERSION: str = "v19.0"
    _api: FacebookAdsApi = None

    @override
    def _set_credentials(self, credentials: Any) -> None:
        """Set platfrom credentials.

        Args:
        ----
            credentials (Any): Provided credentials. Format: {"access_token": "","app_secret": "","app_id": ""}

        """
        self._credentials: Dict[str, str] = cast(Dict[str, str], credentials)

    @override
    def _is_credentials(self) -> bool:
        """Check if credential is valid and reissue token (or other credentials) if needed.

        Returns
        -------
            bool: if can connect

        """
        if not self._credentials:
            return False
        if not self._api:
            self._api = FacebookAdsApi.init(
                access_token=self._credentials.get("access_token", ""),
                app_id=self._credentials.get("app_id", ""),
                app_secret=self._credentials.get("app_secret", ""),
            )
        return self._api is not None

    def _get_ad_account(self, adaccount_id: str) -> Dict[str, Any]:
        """Get ad accounr information.

        Args:
        ----
            adaccount_id (str): adaccount id

        Returns:
        -------
            dict: Advertiser

        """
        result = {}
        if self._is_credentials():
            response = self._http_session.get(
                f"https://graph.facebook.com/{self._API_VERSION}/{adaccount_id}/",
                headers={
                    "Accept": "application/json",
                },
                params={
                    "access_token": self._credentials["access_token"],
                    "fields": "timezone_id,timezone_name,timezone_offset_hours_utc,currency",
                },
                timeout=None,
            )
            response.raise_for_status()

            if response.status_code == 200:
                result = response.json()
            for item in json.loads(response.headers.get("x-business-use-case-usage", "{}")).get(adaccount_id.replace("act_", ""), []):
                if item["type"] == "ads_management":
                    result["rate_limit"] = item
                    break

        return result

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
        result: list[Any] = []
        if self._is_credentials() and self._credentials.get("app_scoped_system_user_id", ""):
            response = self._http_session.get(
                f"https://graph.facebook.com/{self._API_VERSION}/{self._credentials.get('app_scoped_system_user_id', '')}/",
                headers={"Accept": "application/json"},
                params={"access_token": self._credentials["access_token"], "fields": "assigned_ad_accounts"},
                timeout=None,
            )
            response.raise_for_status()
            roles = set(
                [
                    role
                    for account_roles in response.json().get("assigned_ad_accounts", {}).get("data", [])
                    for role in account_roles.get("tasks", [])
                    if account_roles.get("account_id", "") == first_level_id or account_roles.get("id", "") == first_level_id
                ]
            )
            result = list(roles & self.ACCESS_ROLES)
        else:
            result = [self._get_ad_account(first_level_id)]
        return bool(result) and bool(result[0])

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
            first_level_id (str): id for main platfrom identificator to get catalog for.
            second_level_ids (List[str] | None, optional): list of second level elements to get (campaigns e.g.). Defaults to None.
            only_placements (bool, optional): Return only placement in response. Defaults to False.
            no_placements (bool, optional): Does not return placements in response. Defaults to False.
            is_force_update (bool, optional): Force update even if cache is exists. Defaults to False.

        Returns:
        -------
            Dict[str, Any]: platfrom catalog. Structure {"second_level_items":[{"third_level_items":[{"placements":[]}]}]}.

        """
        response: Dict[str, Any] = {"second_level_items": []}

        def __to_utc_date(date_string: str) -> str:
            return datetime.datetime.fromisoformat(date_string).astimezone(pytz.timezone("UTC")).date().isoformat() if date_string else ""

        if self._is_credentials():
            try:
                if not no_placements:
                    # Get all adsets
                    adsets: List[Any] | None = None if is_force_update else self._cache.get_cache(name="meta_adsets", first_level_id=first_level_id)
                    if adsets is None or is_force_update:
                        results = AdAccount(first_level_id).get_ad_sets(
                            fields=[
                                "name",
                                "campaign_id",
                                "status",
                                "start_time",
                                "stop_time",
                                "lifetime_budget",
                                "source_adset",
                            ]
                        )
                        adsets = [result._json for result in results]
                        self._cache.set_cache(
                            name="meta_adsets",
                            value=adsets,
                            ttl=self._CACHE_TTL,
                            first_level_id=first_level_id,
                        )
                    response_adset: List[Any] = sorted(
                        [result for result in adsets if not second_level_ids or result["campaign_id"] in second_level_ids],
                        key=lambda item: item["name"],
                    )

                # Get currency
                currency: str = ""
                adaccount: Dict[str, Any] | None = None if is_force_update else self._cache.get_cache(name="meta_adaccount", first_level_id=first_level_id)
                if adaccount is None or is_force_update:
                    adaccount = self._get_ad_account(first_level_id)
                    self._cache.set_cache(
                        name="meta_adaccount",
                        value=adaccount,
                        ttl=self._CACHE_TTL,
                        first_level_id=first_level_id,
                    )
                    currency = adaccount.get("currency", "")

                if only_placements and not no_placements:
                    # Only lineitems as dict
                    response = {
                        "placements": {
                            item["id"]: {
                                "id": item["id"],
                                "name": item["name"],
                                "status": item["status"].title(),
                                "budget": f"{currency} {(int(item.get('lifetime_budget', 0)) / 100):.2f}",
                                "channel": "Social",
                                "start_date": __to_utc_date(item.get("start_time", "")),
                                "end_date": __to_utc_date(item.get("stop_time", "")),
                            }
                            for item in response_adset
                        }
                    }
                else:
                    # Prepare intermediate dictionary (need to take names later)
                    campaigns_dict: Dict[str, Any] = {}
                    if not no_placements:
                        for item in response_adset:
                            if item["campaign_id"] not in campaigns_dict:
                                campaigns_dict[item["campaign_id"]] = []
                            campaigns_dict[item["campaign_id"]].append(
                                {
                                    "id": item["id"],
                                    "name": item["name"],
                                    "status": item["status"].title(),
                                    "budget": f"{currency} {(int(item.get('lifetime_budget', 0)) / 100):.2f}",
                                    "channel": "Social",
                                    "start_date": __to_utc_date(item.get("start_time", "")),
                                    "end_date": __to_utc_date(item.get("stop_time", "")),
                                    "is_duplicate": len(item.get("source_adset", [])) > 0,
                                    "is_youtube": False,
                                }
                            )
                    # All campaings
                    # It is fatser to get all in one request and then filter
                    campaigns: List[Any] | None = None if is_force_update else self._cache.get_cache(name="meta_campaigns", first_level_id=first_level_id)
                    if campaigns is None or is_force_update:
                        results = AdAccount(first_level_id).get_campaigns(fields=["name", "start_time", "stop_time", "status"])
                        campaigns = [result._json for result in results]
                        self._cache.set_cache(
                            name="meta_campaigns",
                            value=campaigns,
                            ttl=self._CACHE_TTL,
                            first_level_id=first_level_id,
                        )

                    response = {
                        "second_level_items": [
                            {
                                "id": campaign["id"],
                                "name": campaign["name"],
                                "status": campaign["status"].title(),
                                "start_date": __to_utc_date(campaign.get("start_time", "")),
                                "end_date": __to_utc_date(campaign.get("stop_time", "")),
                                "third_level_items": [
                                    {
                                        "id": "",
                                        "name": "",
                                        "status": "",
                                        "placements": [] if no_placements else campaigns_dict[campaign["id"]],
                                    }
                                ],
                            }
                            for campaign in campaigns
                            if (no_placements or campaign["id"] in campaigns_dict) and (not second_level_ids or campaign["id"] in second_level_ids)
                        ]
                    }
            except FacebookRequestError as error:
                # Artifitially slowdown
                if error.api_error_code() == 17:
                    sleep(50)
                raise Exception(json.dumps(error.body() | {"rate_limit": self._get_ad_account(first_level_id).get("rate_limit", {})}))

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
        response: Dict[str, List[Dict[str, Any]]] = {"placements": []}
        if self._is_credentials():
            try:
                results = Campaign(second_level_id).get_ad_sets(
                    fields=[
                        "name",
                        "optimization_goal",
                        "billing_event",
                        "lifetime_budget",
                        "campaign_id",
                        "start_time",
                        "end_time",
                        "status",
                        "pacing_type",
                        "source_adset",
                        "updated_time",
                    ]
                )
                response = {"placements": [result._json for result in results]}
            except FacebookRequestError as error:
                raise Exception(json.dumps(error.body()))
        return response

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
        return AdSet(placement_id)

    @override
    def duplicate_placement(self, first_level_id: str, placement_id: str, suffixes: List[str]) -> List[str]:
        """Duplicate placement.

        Args:
        ----
            first_level_id (str): id for main platfrom identificator to get catalog for.
            placement_id (str): placement id to duplicate.
            suffixes (list): suffixes for placement display names. Number of suffixes will produce number of dublicates.

        Returns:
        -------
            list: list of created placement ids.

        """
        result: List[str] = []
        if self._is_credentials():

            def _callback_success(meta_response: Any) -> None:
                result.append(meta_response.json().get("copied_adset_id", ""))

            if len(suffixes) > 0:
                try:
                    for batch_suffixes in generate_batches(suffixes, self._CHUNK_SIZE):
                        api_batch = self._api.new_batch()
                        for suffix in batch_suffixes:
                            self.get_placement(first_level_id=first_level_id, placement_id=placement_id).create_copy(
                                params={
                                    "deep_copy": True,
                                    "rename_options": {"rename_suffix": suffix},
                                },
                                batch=api_batch,
                                success=_callback_success,
                                failure=_callback_failure,
                            )
                        api_batch.execute()

                except FacebookRequestError as error:
                    raise Exception(json.dumps(error.body()))
        return result

    @override
    def delete_placement(self, first_level_id: str, placement_ids: List[str]) -> List[str]:
        """Delete placement.

        Args:
        ----
            first_level_id (str): id for main platfrom identificator to get catalog for.
            placement_ids (List[str]): placement ids to delete.

        Returns:
        -------
            list: list of deleted placement ids.

        """
        if self._is_credentials():
            for batch_adset_ids in generate_batches(placement_ids, self._CHUNK_SIZE):
                api_batch = self._api.new_batch()
                for adset_id in batch_adset_ids:
                    self.get_placement(first_level_id=first_level_id, placement_id=adset_id).api_delete(batch=api_batch, failure=_callback_failure)
                api_batch.execute()
        return placement_ids

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
        if self._is_credentials():
            for batch_adset_ids in generate_batches(placement_ids, self._CHUNK_SIZE):
                api_batch = self._api.new_batch()
                for adset_id in batch_adset_ids:
                    self.get_placement(first_level_id=first_level_id, placement_id=adset_id).api_update(
                        {AdSet.Field.status: AdSet.Status.paused},
                        batch=api_batch,
                        failure=_callback_failure,
                    )
                api_batch.execute()
        return placement_ids
