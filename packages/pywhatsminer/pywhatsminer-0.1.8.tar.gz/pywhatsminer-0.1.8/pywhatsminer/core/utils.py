from contextlib import suppress

from datetime import datetime, timedelta


def process_response(response: dict) -> dict:
    if response.get("STATUS"):
        match response.get("STATUS"):
            case 'S': 
                response['STATUS'] = 'success'
            case 'E':
                response['STATUS'] = 'error'
            case _:
                response['STATUS'] = None
    
    for key, value in response.items():
        if type(value) == dict:
            response[key] = process_response(value)
        elif type(value) == str:
            response[key] = value.strip()
            
            match value:
                case 'true':
                    response[key] = True
                case 'false':
                    response[key] = False
                case 'enable':
                    response[key] = True
                case 'disable':
                    response[key] = False
                case 'Alive':
                    response[key] = True
                case 'Dead':
                    response[key] = False
                case 'Y':
                    response[key] = True
                case 'N':
                    response[key] = False
                case '':
                    response[key] = None
                    
            if type(response[key]) == str and response[key].isdigit():
                response[key] = int(response[key])  
            with suppress(ValueError, TypeError):
                response[key] = float(response[key]) if not isinstance(response[key], int) else response[key]
        
        match key:
            case 'When':
                response[key] = datetime.fromtimestamp(response[key])
            case 'Uptime':
                response[key] = timedelta(seconds=response[key])
            case 'Elapsed':
                response[key] = timedelta(seconds=response[key])
            case 'Upfreq Complete':
                response[key] = bool(response[key])
            case 'upfreq_complete':
                response[key] = bool(response[key])
            case 'enable':
                response[key] = bool(response[key])
                
    return response