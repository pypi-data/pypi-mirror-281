import argparse
from os.path import dirname,join,exists,realpath
import yaml
import socket
from conversation import Server,ConnectedClient,utils
import loader
import torch

def get_server(root,map_data,hloc_config,server_config):
    return Server(root,map_data,hloc_config,server_config)

def main(root,hloc_config,server_config):
    map_data=loader.load_data(server_config)
    server = get_server(root,map_data,hloc_config,server_config)
    newConnectionsThread=server.set_new_connections(map_data)
    newConnectionsThread.start()

if __name__=='__main__':
    root = dirname(realpath(__file__)).replace('/src','')
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server_config', type=str, default='configs/server.yaml')
    parser.add_argument('-l', '--hloc_config', type=str, default='configs/hloc.yaml')
    args = parser.parse_args()
    with open(args.hloc_config, 'r') as f:
        hloc_config = yaml.safe_load(f)
    with open(args.server_config, 'r') as f:
        server_config = yaml.safe_load(f)
    main(root,hloc_config,server_config)