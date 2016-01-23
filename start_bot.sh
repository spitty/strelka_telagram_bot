#!/bin/bash
source bin/activate
nohup flock -n strelka.lock -c 'python strelka_bot.py 2>&1' >> system.out &
echo $! > strelka.pid
