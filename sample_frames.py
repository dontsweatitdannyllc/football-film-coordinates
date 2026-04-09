import argparse,subprocess

parser=argparse.ArgumentParser()
parser.add_argument('--input',required=True)
parser.add_argument('--fps',type=int,default=10)
parser.add_argument('--out',default='clip_10fps.mp4')
args=parser.parse_args()

cmd=['ffmpeg','-i',args.input,'-filter:v',f'fps={args.fps}',args.out]
subprocess.run(cmd)
print('saved',args.out)
