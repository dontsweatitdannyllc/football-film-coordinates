import argparse, subprocess

parser=argparse.ArgumentParser()
parser.add_argument('--url',required=True)
parser.add_argument('--start',required=True)
parser.add_argument('--end',required=True)
parser.add_argument('--out',default='clip.mp4')
args=parser.parse_args()

cmd=[
'yt-dlp',
'-f','bestvideo[height<=720]+bestaudio/best[height<=720]',
'--download-sections',f'*{args.start}-{args.end}',
'-o',args.out,
args.url
]

subprocess.run(cmd)
print('downloaded',args.out)
