#!/bin/bash

if [ $# -ne 1 ]
then
    echo "Usage: `basename $0` {experiment_name}"
exit
fi

exp=$1
python plot_queue.py --maxy 100 --miny 0 -f ${exp}_sw0-qlen.txt -o ${exp}_queue.png 
python plot_tcpprobe.py -f ${exp}_tcpprobe.txt -o ${exp}_tcp_cwnd_iperf.png -p 5001 
python plot_tcpprobe.py -f ${exp}_tcpprobe.txt -o ${exp}_tcp_cwnd_wget.png -p 80 --sport

