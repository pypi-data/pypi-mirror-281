from pywhatsminer.core.api import WhatsminerAPI, WhatsminerAccessToken
from typing import Any


class Config:
    def __init__(self, client):
        self.client = client
        self.api: WhatsminerAPI = client.api
        self.token: WhatsminerAccessToken = client._access_token
        
        
    def open_ssh(self) -> Any:
        """
        This operation opens miner's SSH server.
        """
        return self.api.exec_command(self.token, "ssh_open")
    

    def close_ssh(self) -> Any:
        """
        This operation closes miner's SSH server.
        """
        return self.api.exec_command(self.token, "ssh_close")
    
    
    def manage_led(self, color: str | None = None, period: int | None = None, duration: int | None = None, start: int | None = None) -> Any:
        """
        This operation manages miner's LED. If no fields are provided, it sets to auto control mode.
        
        Params:
            - color: str = None - LED color. Possible fields: "green", "red"
            - period: int = None - LED flash cycle (in ms)
            - duration: int = None - LED on time in cycle (in ms)
            - start: int = None - LED time offset (in ms)
        """
        
        assert color in ["green", "red"]
        
        if not any([color, period, duration, start]):
            return self.api.exec_command(self.token, "set_led", {"param":"auto"})
        else:
            return self.api.exec_command(self.token, "set_led", {"param":color, "period":period, "duration":duration, "start":start})
        
        
    def change_password(self, old: str, new: str) -> Any:
        """
        This operation changes miner's admin password. Requires old password.
        
        Params:
            - old: str - old password
            - new: str - new password
        """
        return self.api.exec_command(self.token, "update_pwd", {"old":old, "new":new})
    
    
    def set_target_frequency(self, frequency: int) -> Any:
        """
        This operation sets miner's target frequency.
        
        Params:
            - freq: int - target frequency in percent. Range: -100 to 100.
        """
        assert frequency in range(-100, 101)
        
        return self.api.exec_command(self.token, "set_target_freq", {"percent":frequency})
    
    
    def enable_fastboot(self) -> Any:
        """
        This operation enables btminer fastboot. After setting, the next restart of the miner takes effect.
        """
        return self.api.exec_command(self.token, "enable_btminer_fast_boot")
    
    
    def disable_fastboot(self) -> Any:
        """
        This operation disables btminer fastboot. After setting, the next restart of the miner takes effect.
        """
        return self.api.exec_command(self.token, "disable_btminer_fast_boot")
    
    
    def enable_web_pools(self) -> Any:
        """
        This operation allows configuration of pools on web pages with immediate effect.

        """
        return self.api.exec_command(self.token, "enable_web_pools")
    
    
    def disable_web_pools(self) -> Any:
        """
        This operation turns off the configure pools feature on the web page with immediate effect.
        """
        return self.api.exec_command(self.token, "disable_web_pools")
    
    
    def set_hostname(self, hostname: str) -> Any:
        """
        This operation sets miner's hostname, does not take effect until the network is restarted.
        
        Params:
            - hostname: str - new hostname
        """
        return self.api.exec_command(self.token, "set_hostname", {"hostname":hostname})
    
    
    def set_time_zone(self, timezone: str) -> Any:
        """
        This operation sets miner's time zone, does not take effect until the network is restarted.
        
        Params:
            - timezone: str - new timezone (eg. "CST-8")
            - zonename: str - new timezone (eg. "Asia/Shanghai")
        """
        return self.api.exec_command(self.token, "set_timezone", {"timezone":timezone})
    
    
    def load_log(self, ip: str, port: int | str, proto: str) -> Any:
        """
        This operation configures the rsyslog log server. 
        
        Params:
            - ip: str - ip address
            - port: int | str - port
            - proto: str - protocol. Possible fields: "tcp", "udp"
        """
        assert proto in ["tcp", "udp"]
        
        return self.api.exec_command(self.token, "load_log", {"ip":ip, "port":port, "proto":proto})
    
    
    def set_temp_offset(self, offset: int) -> Any:
        """
        This operation sets offset of miner hash board target temperature. 
        
        Params:
            - offset: int - temperature offset in degrees. Range: -30 to 0.
        """
        assert offset in range(-30, 1)
        
        return self.api.exec_command(self.token, "set_temp_offset", {"temp_offset":offset})
    

    def adjust_upfreq_speed(self, speed: int) -> Any:
        """
        This operation sets the upfreq speed, 0 is the normal speed, 9 is the fastest speed. 
        The faster the speed, the greater the final hash rate and power deviation, and the stability may have a certain impact. 
        Fast boot mode cannot be used at the same time.
        
        Params:
            - speed: int - new upfreq speed. Range: 0 to 9.
        """
        assert speed in range(0, 10)
        
        return self.api.exec_command(self.token, "adjust_upfreq_speed", {"upfreq_speed":speed})
    
    
    def set_poweroff_cool(self, poweroff_cool: bool) -> Any:
        """
        This operation sets whether to cool machine when stopping mining.
        
        Params:
            - poweroff_cool: bool - whether to cool machine when stopping mining
        """
        return self.api.exec_command(self.token, "set_poweroff_cool", {"poweroff_cool":1 if poweroff_cool else 0})
    
    
    def set_fan_zero_speed(self, fan_zero_speed: bool) -> Any:
        """
        This operation sets whether the fan speed supports the lowest 0 speed.
        
        Params:
            - fan_zero_speed: bool - whether the fan speed supports the lowest 0 speed
        """
        return self.api.exec_command(self.token, "set_fan_zero_speed", {"fan_zero_speed":1 if fan_zero_speed else 0})