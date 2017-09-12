import os,json

#if not os.path.exists(src_image)
with open('requirement.json') as data_file:
    config = json.load(data_file)

sys_config_list =  ' '.join(config['sys'])

pip_config_list =  ' '.join(config['pip'])

os.system(" dnf install -y "+sys_config_list)
#print(" dnf install -y "+sys_config_list)

print("installed all system dependencies")

os.system("pip3 install "+pip_config_list)
#print("pip3 install "+pip_config_list)

print("installed all python3 dependencies")

