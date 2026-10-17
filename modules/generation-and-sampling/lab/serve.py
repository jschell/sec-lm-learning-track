"""Start the prepared model in the foreground on loopback. Ctrl-C stops it."""
import argparse
import subprocess

from prepare import CONFIG, MODEL, SERVER, model_ready


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=8080)
    parser.add_argument('--threads',type=int,default=4)
    args=parser.parse_args()
    if not 1024<=args.port<=65535 or not 1<=args.threads<=8:
        parser.error('port must be 1024–65535; threads must be 1–8')
    if not SERVER.is_file() or not model_ready():
        parser.error('prepared server/model missing or altered; run prepare.py first')
    command=[str(SERVER),'-m',str(MODEL),'--alias','smollm2-135m-instruct-q8',
             '--host','127.0.0.1','--port',str(args.port),'-t',str(args.threads),
             '-c','1024','-np','1','-ngl','0']
    print('Model:',CONFIG['model'],'Runtime:',CONFIG['runtime_revision'],flush=True)
    try:
        return subprocess.run(command,check=False).returncode
    except KeyboardInterrupt:
        return 0


if __name__=='__main__':
    raise SystemExit(main())
