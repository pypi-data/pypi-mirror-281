from pywhatsminer.core.api import WhatsminerAPI, WhatsminerAccessToken
from pywhatsminer.core.models import PSU
from pywhatsminer.core.utils import process_response

from typing import Any


class Power:
    def __init__(self, client):
        self.client = client
        self.api: WhatsminerAPI = client.api
        self.token: WhatsminerAccessToken = client._access_token
        
    
    def on(self) -> Any:
        """
        This operation simply starts mining and turns on the power output of the power board.
        """
        return self.api.exec_command(self.token, "power_on")
    

    def off(self, respbefore: bool = False) -> Any:
        """
        This operation simply stops mining and turns off the power output of the power board.
        There was no power outage on the control board
        
        Params:
            - respbefore: bool = False - when true, the miner returns the data first and then closes the hashboard, otherwise close the hashboard first and then return the data.
        """
        return self.api.exec_command(self.token, "power_off", {"respbefore": respbefore})
        
    
    def restart(self) -> Any:
        """
        This operation restarts the miner.
        """
        return self.api.exec_command(self.token, "restart_btminer")
    
    
    def switch_mode(self, mode: str) -> Any:
        """
        This operation changes miner's power mode.
        
        Params:
            - mode: str - new power mode. Possible fields: "low", "normal", "high"
        """
        assert mode in ["low", "normal", "high"]
        
        return self.api.exec_command(self.token, f"set_{mode}_power")


    def get_psu(self) -> PSU:
        """
        This method returns miner's power system status.
        """
        data = process_response(self.api.exec_command(self.token, "get_psu"))

        return PSU(*data['Msg'].values())
    
    
    def set_percent(self, percent: int) -> Any:
        """
        Temporarily set the power percent based on the current running power. 
        It is recommended to be used for temporary adjustment. Long run maybe unstable. 
        If you want the machine run for a long time in low power percent, see `Client.Power.adjust_limit()`
        
        Params:
            - percent: int - new power output percentage. Range: 0 to 100.
        """
        return self.api.exec_command(self.token, "set_power_pct", {"percent": percent})
    
    
    def adjust_limit(self, limit: int) -> Any:
        """
        This operation sets the upper limit of the miner's power. 
        Not higher than the ordinary power of the machine.
        If the Settings take effect, the machine will restart.

        Params:
            - limit: int - new power limit percentage. Range: 0 to 99999.
        """
        assert limit in range(0, 100000)
        
        return self.api.exec_command(self.token, "adjust_power_limit", {"power_limit":limit})
    
    
    def pre_power_on(self) -> Any:
        """
        The miner can be preheated by `pre_power_on` before `power_on`, so that the machine
        can quickly enter the full power state when "power on" is used. 
        
        You can also use this
        command to query the pre power on status. Make sure `power_off` btminer before
        `pre_power_on`. 
        
        Response:
            - complete: bool
            - query: str - query the status. Possible fields: "wait for adjust temp", "adjust complete", "adjust continue"

        1. "wait for adjust temp": The temperature adjustment of the miner is not completed. 
        2. "adjust complete": The temperature adjustment of the miner is completed, and miner can be power on.
        3. "adjust continue": Miner is adjusting the temperature while waiting to end. 
        
        The value of "complete" is true after the temperature adjustment is complete.
        """
        return self.api.exec_command(self.token, "pre_power_on")
