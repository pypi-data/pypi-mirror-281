from warskald import utils, EnvironmentProps, get_inputs, AttrDict
from warskald.utils import p_exists, p_join

ENV_PROPS = EnvironmentProps()
APP_NAME = 's3cli'
APP_PROPS = ENV_PROPS.get(APP_NAME)

def set_cfg_value(key: str, value: str) -> None:
    
    ENV_PROPS.set('application.properties', [APP_NAME, key], value)
    APP_PROPS.update({key: value})

def handle_cfg(cfg_arg: str) -> None:
    if(not isinstance(cfg_arg, str)):
        raise ValueError('The --cfg option must follow the format of --cfg <action> [<key value pairts>]\neg: --cfg set arg1 value1, arg2 value2')
        
    action = cfg_arg.split()[0]
    
    if(action not in ['get', 'set']):
        raise ValueError('The action must be either "get" or "set"')
    
    pairs_str = cfg_arg.split()[1:]
    
    pairs = [pair.split(',') for pair in pairs_str]
    
    for key, value in pairs:
        if(action == 'set'):
            set_cfg_value(key, value)
        else:
            print(APP_PROPS.get(key))
            
def execute_cmd(*args) -> None:
    cmd = 'aws ' + ' '.join(args)
    utils.cmdx(cmd)

def valid_args(*args) -> bool:
    return all([isinstance(arg, str) for arg in args])

def handle_action(args: AttrDict | str) -> None:
    if(isinstance(args, str)):
        args = AttrDict()
        
    service = args.s or APP_PROPS.current_service or 's3api'
    if(service == 's3api'):
        src_bucket = args.b or APP_PROPS.current_source_bucket
        region = args.r or APP_PROPS.current_region
        profile = args.p or APP_PROPS.current_profile
        cmd = args.c or APP_PROPS.current_command
        
        if(cmd == 'ls' and valid_args([src_bucket, region, profile])):
            cmd = 'list-buckets'
            
            execute_cmd(service, cmd, f'--bucket {src_bucket}', f'--region {region}', f'--profile {profile}')
            
def main():
    args = get_inputs()
    
    if(args.h):
        print('Usage: s3cli [-h] [-c] [-s] [-b] [-r] [-p] [--cfg]')
        print('Options:')
        print('  -h, --help    Show this help message and exit')
        print('  -c            The command to execute')
        print('  -s            The service to use')
        print('  -b            The source bucket')
        print('  -r            The region to use')
        print('  -p            The profile to use')
        print('  --cfg         Set or get configuration values')
        return
    
    if(args.cfg):
        handle_cfg(args.cfg)
    else:
        handle_action(args)
    
if(__name__ == "__main__"):
    main()