from warskald import utils, EnvironmentProps, get_inputs, AttrDict
from warskald.utils import p_exists, p_join

ENV_PROPS = EnvironmentProps()
APP_NAME = 's3cli'
APP_PROPS = ENV_PROPS.get(APP_NAME)

def debug_print(*args) -> None:
    if(APP_PROPS.debug):
        print(*args)

def set_cfg_value(key: str, value: str) -> None:
    print(f'Setting configuration value: {key} = {value}')
    
    ENV_PROPS.set('application.properties', [APP_NAME, key], value)
    APP_PROPS.update({key: value})
    
def del_cfg_value(key: str) -> None:
    print(f'Deleting configuration value: {key}')
    
    ENV_PROPS.delete('application.properties', [APP_NAME, key])
    APP_PROPS.pop(key)

def handle_cfg(cfg_arg: str) -> None:
    if(not isinstance(cfg_arg, str)):
        raise ValueError('The --cfg option must follow the format of --cfg <action> [<key value pairts>]\neg: --cfg set arg1 value1, arg2 value2')
        
    action = cfg_arg.split()[0]
    
    if(action not in ['get', 'set', 'del']):
        raise ValueError('The action must be either "get", "set", or "del"')
    
    pair_values = cfg_arg.split()[1:]
    
    
    if(action in ['get','set']):
        kv_pairs = [pair.split(',') for pair in pair_values]
        for key, value in kv_pairs:
            if(action == 'set'):
                set_cfg_value(key, value)
            else:
                print(f'key = {APP_PROPS.get(key)}')
    else:
        for key in pair_values:
            del_cfg_value(key)
            
def execute_cmd(*args) -> None:
    cmd = 'aws ' + ' '.join(args)
    debug_print(f'Executing command: {cmd}')
    utils.cmdx(cmd)

def valid_args(*args) -> bool:
    valid = all([isinstance(arg, str) for arg in args])
    if(not valid):
        debug_print('Invalid arguments')
        debug_print(args)
    return valid

def handle_action(args: AttrDict | str) -> None:
    if(isinstance(args, str)):
        args = AttrDict()
        
    service = args.s or APP_PROPS.current_service or 's3api'
    if(service == 's3api'):
        debug_print('Using s3api')
        
        src_bucket = args.b or APP_PROPS.current_source_bucket
        region = args.r or APP_PROPS.current_region
        profile = args.p or APP_PROPS.current_profile
        cmd = args.c or APP_PROPS.current_command
        
        debug_print(f'Command: {cmd}, Bucket: {src_bucket}, Region: {region}, Profile: {profile}')
        
        if(cmd == 'ls' and valid_args([src_bucket, region, profile])):
            cmd = 'list-buckets'
            debug_print(f'Command recognized: {cmd}')    
            execute_cmd(service, cmd, f'--bucket {src_bucket}', f'--region {region}', f'--profile {profile}')
            
        elif(cmd == 'get-bucket-acl' and valid_args([src_bucket, region, profile])):
            debug_print(f'Command recognized: {cmd}')    
            execute_cmd(service, cmd, f'--bucket {src_bucket}', f'--region {region}', f'--profile {profile}')
            
        else:
            debug_print(f'Command not explicitly recognized: {cmd}\nAttempting default command format')
            if(valid_args([cmd, src_bucket, region, profile])):
                execute_cmd(service, cmd, f'--bucket {src_bucket}', f'--region {region}', f'--profile {profile}')
            
def main():
    args = get_inputs()
    
    if(args.debug):
        APP_PROPS.debug = True
    
    if(args.h):
        print('Usage: s3cli [-h] [-c] [-s] [-b] [-r] [-p] [--cfg]')
        print('Options:')
        print('  -h, --help    Show this help message and exit')
        print('  -c            The command to execute')
        print('  -s            The service to use')
        print('  -b            The source bucket')
        print('  -r            The region to use')
        print('  -p            The profile to use')
        print('  -d            The destination bucket')
        print('  -debug        Debug mode')
        print('  --cfg         Set or get configuration values')
        return
    
    if(args.cfg):
        handle_cfg(args.cfg)
    else:
        handle_action(args)
    
if(__name__ == "__main__"):
    main()