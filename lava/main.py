from net.lava import start
from loguru import logger
import argparse

def main():
    import sys
    import os
    from PIL import Image as img

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--motd", default="Lava, python based mojang account verification server.", help="Set motd for server. Displays in server list.")
    parser.add_argument("-i", "--icon-path", default="./icon.png", help="Server icon. Displays in server list.")
    parser.add_argument("-dR", "--debug-rotation", type=str, default="10 MB", help="Log rotation time. Format: '1 week', '1 MB'.")
    parser.add_argument("-l", "--log-file", type=str, default="latest.log", help="Log file.")
    parser.add_argument("-L", "--log-level", type=str, default="DEBUG", help="Log level.")
    parser.add_argument("-H", "--host", type=str, default="localhost", help="Host to listen on.")
    parser.add_argument("-p", "--port", type=int, default=25565, help="Port to listen on.")
    parser.add_argument("-s", "--secure-mode", type=str2bool, default=False, help="Secure mode. Do not secure info.")
    parser.add_argument("-a", "--api", type=str, required=True, help="URL to send request with user info.")
    parser.add_argument("-A", "--api-token", type=str, required=True, help="Server token. Used for authorize server.")
    args = parser.parse_args()
    
    logger.add(args.log_file, rotation=args.debug_rotation, level=args.log_level)
    logger.info("Starting Lava on {0}({1}).".format(args.host, args.port))

    logger.info("Checking files.")

    image = None

    if not os.path.exists(args.icon_path):
        logger.warning("Icon file doesn't exists. ({0})".format(args.icon_path))
    
    else:
        image = img.open(args.icon_path)
        size = get_image_size(image)
        if size[0] != 64 and image:
            logger.warning("Icon width isn't equals 64 pixel")
            image = None
        if size[1] != 64 and image:
            logger.warning("Icon height isn't equals 64 pixel")
            image = None

    if args.secure_mode:
        args.api_token = encode_token(args.api_token)

    logger.info("Constructing protocol.")
    logger.info("Using {0} as HTTPS API.".format(args.api))
    logger.info("Log rotation is {0}".format(args.debug_rotation))
    logger.info("Secure mode is {0}.".format(args.secure_mode and "enabled" or "disabled"))
    logger.info("API token is {0}.".format(args.api_token))
    start(logger, args, image)

def get_image_size(image):

    width, height = image.size

    return (width, height)

def str2bool(string):

    if isinstance(string, bool):
       return string
    if string.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif string.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def encode_token(token):

    length = len(token)

    if length != 20:
        raise argparse.ArgumentTypeError("API Token length must be 20")
    
    encrypted = token[:5] + '***************'
    return encrypted

main()
