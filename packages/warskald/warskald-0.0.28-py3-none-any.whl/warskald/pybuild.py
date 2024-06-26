from warskald import utils
from warskald.ws_config import EnvPropsReader
from warskald.attr_dict import AttrDict

ENV_PROPS = EnvPropsReader()
APP_NAME = 'pybuild'
APP_PROPS = ENV_PROPS.get(APP_NAME)

def main():
    
    args = utils.get_inputs()
    ENV_PROPS.set('application.properties', 'pybuild.test', 'test')
    
    
    

if(__name__ == '__main__'):
    main()