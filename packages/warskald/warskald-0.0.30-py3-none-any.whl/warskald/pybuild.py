import configparser
import os
import re
import time

from typing import Any
from warskald import utils
from warskald.ws_config import EnvironmentProps
from warskald.attr_dict import AttrDict

ENV_PROPS = EnvironmentProps()
APP_NAME = 'pybuild'
APP_PROPS = ENV_PROPS.get(APP_NAME)

PY_ALIAS = ENV_PROPS.get('aliases.python')

def validate_version(version: Any) -> str:
    if(version is None):
        return '0.0.0'
    if(isinstance(version, str)):
        matches = re.match(r'^\d+\.\d+\.\d+$', version)
        if(matches):
            return version
        else:
            return '0.0.0'
        
def validate_app_name(app_name: str) -> bool:
    pypirc = configparser.ConfigParser()
    pypirc.read(os.path.expanduser('~/.pypirc'))
    
    return app_name in pypirc.sections()

def install_app(local: bool = False) -> None:
    if(local):
        print(f'Installing {APP_PROPS.app_name} from local dist directory')
        dist_path = os.path.join(APP_PROPS.app_dir, 'dist')
        whl_path = os.path.join(dist_path, f'{APP_NAME}-{APP_PROPS.app_version}-py3-none-any.whl')
        if(not os.path.exists(whl_path)):
            raise FileNotFoundError(f'Wheel file not found at {whl_path}')
        utils.cmdx(f'{PY_ALIAS} -m pip install {whl_path} --upgrade')
    else:
        print(f'Installing {APP_PROPS.app_name} from PyPi')
        # Allow time for upload to PyPi
        time.sleep(3)
        
        utils.cmdx(f'{PY_ALIAS} -m pip install {APP_NAME} --upgrade')
        
def get_version() -> tuple[str, str]:
    """ Retrieves the current version from the app properties and returns it 
        along with the new version if the appropriate terminal commands are provided.

    Returns:
        tuple[str, str]:  A tuple containing the current version and the new version
    """
        
    args = utils.get_inputs()
    version = validate_version(APP_PROPS.get('app_version'))
    version_nums = version.split('.')
    
    if(args.M):
        version_nums[0] = str(int(version_nums[0]) + 1)
        version_nums[1] = '0'
        version_nums[2] = '0'
    elif(args.m):
        version_nums[1] = str(int(version_nums[1]) + 1)
        version_nums[2] = '0'
    elif(args.p):
        version_nums[2] = str(int(version_nums[2]) + 1)
        
    return version, '.'.join(version_nums)

def main():
    args = utils.get_inputs()
    
    if(args.h or args.help):
        print('Usage: pybuild [-h] [-c] [-u] [-l] [-M] [-m] [-p]')
        print('Options:')
        print('  -h, --help    Show this help message and exit')
        print('  -c, --clear   Clear the dist directory')
        print('  -u, --upload  Upload to PyPi')
        print('  -l, --local   Install from local dist directory')
        print('  -M            Increment the major version')
        print('  -m            Increment the minor version')
        print('  -p            Increment the patch version')
        return
    
    if(isinstance(APP_PROPS.app_dir, str) and os.path.exists(APP_PROPS.app_dir)):
    
        old_version, new_version = get_version()
        
        if(args.c or args.clear):
            dist_path = os.path.join(APP_PROPS.app_dir, 'dist')
            utils.cmdx(f'rm -rf {dist_path}')
        
        setup_path = os.path.join(APP_PROPS.app_dir, 'setup.py')
        
        if(os.path.exists(setup_path)):
            utils.cmdx(f'{PY_ALIAS} {setup_path} {new_version}')
            
        if(old_version != new_version):
            APP_PROPS.app_version = new_version
            ENV_PROPS.set('application.properties', [APP_NAME, 'app_version'], new_version)
            print(f'Updated version from {old_version} to {new_version}')
        else:
            print(f'Version remains at {old_version}')
            
        if(args.u or args.upload):
            print('Uploading to PyPi')
            app_name = APP_PROPS.app_name
            if(isinstance(app_name, str) and validate_app_name(app_name)):
                utils.cmdx(f'twine upload --repository {app_name} dist/*')
                install_app(False)
            else:
                raise ValueError('App name not found in application properties')
            
        elif(args.l or args.local):
            install_app(True)
    
    else:
        raise FileNotFoundError(f'Application directory not found: {APP_PROPS.app_dir}\nPlease set the app_dir property in the application properties file')
            

if(__name__ == '__main__'):
    main()