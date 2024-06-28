import re
from typing import Any, TypeVar

from communex.client import CommuneClient
from communex.key import check_ss58_address
from communex.types import (
    ModuleInfoWithOptionalBalance,
    NetworkParams,
    Ss58Address,
    SubnetParamsWithEmission,
    SubnetParamsMaps,
)

IPFS_REGEX = re.compile(r"^Qm[1-9A-HJ-NP-Za-km-z]{44}$")

T = TypeVar("T")

def get_map_modules(
    client: CommuneClient,
    netuid: int = 0,
    include_balances: bool = False,
) -> dict[str, ModuleInfoWithOptionalBalance]:
    """
    Gets all modules info on the network
    """

    request_dict: dict[Any, Any] = {
        "SubspaceModule": [
            ("StakeFrom", [netuid]),
            ("Keys", [netuid]),
            ("Name", [netuid]),
            ("Address", [netuid]),
            ("RegistrationBlock", [netuid]),
            ("DelegationFee", [netuid]),
            ("Emission", []),
            
            ("Incentive", []),
            ("Dividends", []),
            ("LastUpdate", []),
            ("Metadata", [netuid]),
        ],
    }
    if include_balances:
        request_dict["System"] = [("Account", [])]

    bulk_query = client.query_batch_map(request_dict)
   
    (
        ss58_to_stakefrom,
        uid_to_key,
        uid_to_name,
        uid_to_address,
        uid_to_regblock,
        ss58_to_delegationfee,
        uid_to_emission,
        uid_to_incentive,
        uid_to_dividend,
        uid_to_lastupdate,
        ss58_to_balances,
        uid_to_metadata,
    ) = (
        bulk_query.get("StakeFrom", {}),
       bulk_query.get("Keys", {}),
        bulk_query["Name"],
        bulk_query["Address"],
        bulk_query["RegistrationBlock"],
        bulk_query["DelegationFee"],
        bulk_query["Emission"],
        bulk_query["Incentive"],
        bulk_query["Dividends"],
        bulk_query["LastUpdate"],
        bulk_query.get("Account", {}),
        bulk_query.get("Metadata", {}),
    )

    result_modules: dict[str, ModuleInfoWithOptionalBalance] = {}

    for uid, key in uid_to_key.items():
        key = check_ss58_address(key)

        name = uid_to_name[uid]
        address = uid_to_address[uid]
        emission = uid_to_emission[netuid][uid]
        incentive = uid_to_incentive[netuid][uid]
        dividend = uid_to_dividend[netuid][uid]
        regblock = uid_to_regblock[uid]
        stake_from = ss58_to_stakefrom.get(key, [])
        last_update = uid_to_lastupdate[netuid][uid]
        delegation_fee = ss58_to_delegationfee.get(
            key, 20
        )  # 20% default delegation fee
        metadata = uid_to_metadata.get(uid, None)

        balance = None
        if include_balances and ss58_to_balances is not None:  # type: ignore
            balance_dict = ss58_to_balances.get(key, None)
            if balance_dict is not None:
                assert isinstance(balance_dict["data"], dict)
                balance = balance_dict["data"]["free"]
            else:
                balance = 0
        stake = sum(stake for _, stake in stake_from)

        module: ModuleInfoWithOptionalBalance = {
            "uid": uid,
            "key": key,
            "name": name,
            "address": address,
            "emission": emission,
            "incentive": incentive,
            "dividends": dividend,
            "stake_from": stake_from,
            "regblock": regblock,
            "last_update": last_update,
            "balance": balance,
            "stake": stake,
            "delegation_fee": delegation_fee,
            "metadata": metadata,
        }

        result_modules[key] = module
    return result_modules

def to_snake_case(d: dict[str, T]) -> dict[str, T]:
    """
    Converts a dictionary with camelCase keys to snake_case keys
    """
    def snakerize(camel: str) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', camel).lower()
    snaked: dict[str, T] = {snakerize(k): v for k, v in d.items()}
    return snaked


def get_map_subnets_params(
    client: CommuneClient, block_hash: str | None = None
) -> dict[int, SubnetParamsWithEmission]:
    """
    Gets all subnets info on the network
    """

    bulk_query = client.query_batch_map(
        {
            "SubspaceModule": [
                ("ImmunityPeriod", []),
                ("MinAllowedWeights", []),
                ("MaxAllowedWeights", []),
                ("MinStake", []),
                ("SubnetEmission", []),
                ("Tempo", []),
                ("MaxAllowedUids", []),
                ("TargetRegistrationsInterval", []),
                ("TargetRegistrationsPerInterval", []),
                ("MaxRegistrationsPerInterval", []),
                ("Founder", []),
                ("FounderShare", []),
                ("IncentiveRatio", []),
                ("TrustRatio", []),
                ("SubnetNames", []),
                ("MaxWeightAge", []),
                ("BondsMovingAverage", []),
                ("MaximumSetWeightCallsPerEpoch", []),
                ("AdjustmentAlpha", []),
            ],
                "GovernanceModule": [
                    ("SubnetGovernanceConfig", []),
                ]
        },
        block_hash,
    )
    subnet_maps: SubnetParamsMaps = {
        "netuid_to_emission": bulk_query["SubnetEmission"],
        "netuid_to_tempo": bulk_query["Tempo"],
        "netuid_to_immunity_period": bulk_query["ImmunityPeriod"],
        "netuid_to_min_allowed_weights": bulk_query["MinAllowedWeights"],
        "netuid_to_max_allowed_weights": bulk_query["MaxAllowedWeights"],
        "netuid_to_max_allowed_uids": bulk_query["MaxAllowedUids"],
        "netuid_to_min_stake": bulk_query["MinStake"],
        "netuid_to_founder": bulk_query["Founder"],
        "netuid_to_founder_share": bulk_query["FounderShare"],
        "netuid_to_incentive_ratio": bulk_query["IncentiveRatio"],
        "netuid_to_trust_ratio": bulk_query["TrustRatio"],
        "netuid_to_name": bulk_query["SubnetNames"],
        "netuid_to_max_weight_age": bulk_query["MaxWeightAge"],
        "netuid_to_vote_mode": bulk_query["SubnetGovernanceConfig"],
        "netuid_to_adjustment_alpha": bulk_query["AdjustmentAlpha"],
        "netuid_to_bonds_ma": bulk_query.get("BondsMovingAverage", {}),
        "netuid_to_maximum_set_weight_calls_per_epoch": bulk_query.get("MaximumSetWeightCallsPerEpoch", {}),
        "netuid_to_target_registrations_per_interval": bulk_query.get("TargetRegistrationsPerInterval", {}),
        "netuid_to_target_registrations_interval": bulk_query.get("TargetRegistrationsInterval", {}),
        "netuid_to_max_registrations_per_interval": bulk_query.get("MaxRegistrationsPerInterval", {}),
    }
    result_subnets: dict[int, SubnetParamsWithEmission] = {}

    default_target_registrations_interval = 200
    default_target_registrations_per_interval = int(default_target_registrations_interval / 2)
    default_max_registrations_per_interval = 42
    for netuid, name in subnet_maps["netuid_to_name"].items():

        subnet: SubnetParamsWithEmission = {
            "name": name,
            "founder": subnet_maps["netuid_to_founder"][netuid],
            "founder_share": subnet_maps["netuid_to_founder_share"][netuid],
            "immunity_period": subnet_maps["netuid_to_immunity_period"][netuid],
            "incentive_ratio": subnet_maps["netuid_to_incentive_ratio"][netuid],
            "max_allowed_uids": subnet_maps["netuid_to_max_allowed_uids"][netuid],
            "max_allowed_weights": subnet_maps["netuid_to_max_allowed_weights"][netuid],
            "min_allowed_weights": subnet_maps["netuid_to_min_allowed_weights"][netuid],
            "min_stake": subnet_maps["netuid_to_min_stake"][netuid],
            "tempo": subnet_maps["netuid_to_tempo"][netuid],
            "trust_ratio": subnet_maps["netuid_to_trust_ratio"][netuid],
            "emission": subnet_maps["netuid_to_emission"][netuid],
            "max_weight_age": subnet_maps["netuid_to_max_weight_age"][netuid],
            "vote_mode": subnet_maps["netuid_to_vote_mode"][netuid]["vote_mode"],
            "adjustment_alpha": subnet_maps["netuid_to_adjustment_alpha"][netuid],
            "bonds_ma": subnet_maps["netuid_to_bonds_ma"].get(netuid, None),
            "maximum_set_weight_calls_per_epoch": subnet_maps["netuid_to_maximum_set_weight_calls_per_epoch"].get(netuid, 30),
            "target_registrations_per_interval": subnet_maps["netuid_to_target_registrations_per_interval"].get(netuid, default_target_registrations_per_interval),
            "target_registrations_interval": subnet_maps["netuid_to_target_registrations_interval"].get(netuid, default_target_registrations_interval),
            "max_registrations_per_interval": subnet_maps["netuid_to_max_registrations_per_interval"].get(netuid, default_max_registrations_per_interval),
        }

        result_subnets[netuid] = subnet

    return result_subnets


def get_global_params(c_client: CommuneClient) -> NetworkParams:
    """
    Returns global parameters of the whole commune ecosystem
    """

    query_all = c_client.query_batch(
        {
            "SubspaceModule": [
                ("MaxAllowedSubnets", []),
                ("MaxAllowedModules", []),
                ("MaxRegistrationsPerBlock", []),
                ("MaxNameLength", []),
                ("FloorDelegationFee", []),
                ("MaxAllowedWeightsGlobal", []),
                ("SubnetStakeThreshold", []),
                ("MinWeightStake", []),
                ("MinNameLength", []),
                ("BurnConfig", []),
                ("FloorFounderShare", []),
            ],
            "GovernanceModule": [
                ("GlobalGovernanceConfig", []),
                ("GeneralSubnetApplicationCost", []),
                ("Curator", []),
            ]
        }
    )
    governance_config: dict[str, int] = query_all["GlobalGovernanceConfig"] # type: ignore
    global_params: NetworkParams = {
        "max_allowed_subnets": int(query_all["MaxAllowedSubnets"]),
        "max_allowed_modules": int(query_all["MaxAllowedModules"]),
        "max_registrations_per_block": int(query_all["MaxRegistrationsPerBlock"]),
        "max_name_length": int(query_all["MaxNameLength"]),
        "min_burn": int(query_all["BurnConfig"]["min_burn"]), # type: ignore
        "max_burn": int(query_all["BurnConfig"]["max_burn"]), # type: ignore
        "min_weight_stake": int(query_all["MinWeightStake"]),
        "floor_delegation_fee": int(query_all["FloorDelegationFee"]),
        "max_allowed_weights": int(query_all["MaxAllowedWeightsGlobal"]),
        "curator": Ss58Address(query_all["Curator"]),
        "proposal_cost": int(governance_config["proposal_cost"]),
        "proposal_expiration": int(governance_config["proposal_expiration"]),
        "subnet_stake_threshold": int(query_all["SubnetStakeThreshold"]),
        "min_name_length": int(query_all["MinNameLength"]),
        "floor_founder_share": int(query_all["FloorFounderShare"]),
        "general_subnet_application_cost": int(query_all["GeneralSubnetApplicationCost"]),


    }
    return global_params


def concat_to_local_keys(
    balance: dict[str, int], local_key_info: dict[str, Ss58Address]
) -> dict[str, int]:
    key2: dict[str, int] = {
        key_name: balance.get(key_address, 0)
        for key_name, key_address in local_key_info.items()
    }

    return key2


def local_keys_to_freebalance(
    c_client: CommuneClient,
    local_keys: dict[str, Ss58Address],
) -> dict[str, int]:
    query_all = c_client.query_batch_map(
        {
            "System": [("Account", [])],
        }
    )
    balance_map = query_all["Account"]

    format_balances: dict[str, int] = {
        key: value["data"]["free"]
        for key, value in balance_map.items()
        if "data" in value and "free" in value["data"]
    }

    key2balance: dict[str, int] = concat_to_local_keys(format_balances, local_keys)

    return key2balance


def local_keys_to_stakedbalance(
    c_client: CommuneClient,
    local_keys: dict[str, Ss58Address],
    netuid: int = 0,
) -> dict[str, int]:
    query_all = c_client.query_batch_map(
        {
            "SubspaceModule": [("StakeTo", [netuid])],
        }
    )

    staketo_map = query_all["StakeTo"]

    format_stake: dict[str, int] = {
        key: sum(stake for _, stake in value) for key, value in staketo_map.items()
    }

    key2stake: dict[str, int] = concat_to_local_keys(format_stake, local_keys)

    return key2stake


def local_keys_allbalance(
    c_client: CommuneClient,
    local_keys: dict[str, Ss58Address],
    netuid: int | None = None,
) -> tuple[dict[str, int], dict[str, int]]:
    staketo_maps: list[Any] = []
    query_result = c_client.query_batch_map(
        {
            "SubspaceModule": [("SubnetNames", [])],
            "System": [("Account", [])],
        }
    )
    balance_map = query_result["Account"]
    all_netuids = list(query_result["SubnetNames"].keys())

    # update for all subnets
    netuids = all_netuids if netuid is None else [netuid]
    for uid in netuids:
        query_result = c_client.query_batch_map(
            {
                "SubspaceModule": [
                    ("StakeTo", [uid]),
                ],
            }
        )
        staketo_map = query_result.get("StakeTo", {})
        staketo_maps.append(staketo_map)

    format_balances: dict[str, int] = {
        key: value["data"]["free"]
        for key, value in balance_map.items()
        if "data" in value and "free" in value["data"]
    }

    key2balance: dict[str, int] = concat_to_local_keys(format_balances, local_keys)

    merged_staketo_map: dict[Any, Any] = {}

    # Iterate through each staketo_map in the staketo_maps list
    for staketo_map in staketo_maps:
        # Iterate through key-value pairs in the current staketo_map
        for key, value in staketo_map.items():
            # If the key is not present in the merged dictionary, add it
            if key not in merged_staketo_map:
                merged_staketo_map[key] = value
            else:
                # If the key exists, extend the existing list with the new values
                merged_staketo_map[key].extend(value)

    format_stake: dict[str, int] = {
        key: sum(stake for _, stake in value)
        for key, value in merged_staketo_map.items()
    }

    key2stake: dict[str, int] = concat_to_local_keys(format_stake, local_keys)

    key2balance = {
        k: v
        for k, v in sorted(key2balance.items(), key=lambda item: item[1], reverse=True)
    }

    key2stake = {
        k: v
        for k, v in sorted(key2stake.items(), key=lambda item: item[1], reverse=True)
    }

    return key2balance, key2stake
