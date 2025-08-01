import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='AWS EC2 Cost Monitor')
    parser.add_argument(
        '--region', type=str, default='eu-central-1', help='AWS region to use'
    )
    parser.add_argument('--threshold', type=float, default=5.0,
                        help='CPU utilization threshold for idle instances')
    args = parser.parse_args()
    return args


args = parse_args()
