import yaml

def conf():
    
    conf_path = 'utils/config.yaml'
    
    with open(conf_path) as f:
        conf = yaml.safe_load(f.read())

    return conf

#if __name__=='__main__':
#    conf()
