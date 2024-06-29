from dataclasses import dataclass
from dataclasses_json import dataclass_json

from datetime import datetime, timedelta


@dataclass_json
@dataclass
class Summary:
    elapsed: int
    mhs_avg: float
    mhs_5s: float
    mhs_1m: float
    mhs_5m: float
    mhs_15m: float
    hs_rate: float
    accepted: int
    rejected: int
    total_mh: float
    temperature: float
    avg_frequency: int
    fan_speed_in: int
    fan_speed_out: int
    power_watts: int
    power_rate: float
    pool_rejected_percent: float
    pool_stale_percent: float
    uptime: timedelta
    target_frequency: int
    target_mhs: float
    env_temp: float
    power_mode: str
    factory_ghs: int
    power_limit: int
    chip_temp_min: float
    chip_temp_max: float
    chip_temp_avg: float
    btminer_fast_boot_enabled: str
    upfreq_complete: bool
    

# TODO: Validate models, maybe incorrect. Needs some tests.
@dataclass_json
@dataclass
class Status:
    miner_off: bool
    miner_off_reason: str
    miner_off_time: int
    firmware_version: str
    power_mode: str
    power_limit_set: bool
    hash_percent: int


@dataclass_json
@dataclass
class PSU:
    name: str
    hardware_version: str
    software_version: str 
    model: str
    enabled: bool
    iin: int
    vin: int
    pin: int
    fan_speed: int
    serial_no: str
    vendor: int
    temperature: float
    
    
@dataclass_json
@dataclass
class Api:
    version: str
    firmware_version: str
    platform: str
    chip: str
    
    
@dataclass_json
@dataclass
class DevDetail:
    id: int
    name: str
    driver: str
    kernel: str
    model: str
    
    
@dataclass_json
@dataclass
class DevDetails:
    details: list[DevDetail]
    
    
@dataclass_json
@dataclass
class Dev:
    asc: int
    slot: int
    enabled: bool
    is_alive: bool
    temperature: float
    chip_frequency: int
    mhs_av: float
    mhs_5s: float
    mhs_1m: float
    mhs_5m: float
    mhs_15m: float
    hs_rate: float
    factory_ghs: int
    upfreq_complete: bool
    effective_chips: int
    pcb_serial_no: str
    chip_data: str
    chip_temp_min: float
    chip_temp_max: float
    chip_temp_avg: float
    chip_vol_diff: int
    

@dataclass_json
@dataclass
class Devs:
    devs: list[Dev]
    

@dataclass_json
@dataclass
class Pool:
    id: int
    url: str
    is_alive: bool
    priority: int
    quota: int
    getworks: int
    accepted: int
    rejected: int
    works: int
    discarded: int
    stale: int
    get_failures: int
    remote_failures: int
    user: str
    last_share_time: datetime
    stratum_is_active: bool
    stratum_difficulty: float
    pool_rejected_percent: float
    pool_stale_percent: float
    bad_works: int
    current_block_height: int
    current_block_version: int
    to_remove: bool
    

@dataclass_json
@dataclass
class Pools:
    pools: list[Pool]
    
    
@dataclass_json
@dataclass
class Info:
    ntp: list[str] | None = None
    ip: str | None = None
    proto: str | None = None
    netmask: str | None = None
    gateway: str | None = None
    dns: str | None = None
    hostname: str | None = None
    mac: str | None = None
    ledstat: str | None = None
    minersn: str | None = None
    powersn: str | None = None
    
    
@dataclass_json
@dataclass
class ErrorCode:
    code: int
    appeared_at: datetime


@dataclass_json
@dataclass
class Errors:
    codes = list[ErrorCode]