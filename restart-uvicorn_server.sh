#!/bin/bash
source /home/dev/Projects/alt-search/backend/venv/bin/activate
cd /home/dev/Projects/alt-search/backend
PID=$(ps aux | grep 'uvicorn main:app' | grep -v grep | awk {'print $2'} | xargs)
if [ "$PID" != "" ]
then
kill -9 $PID
sleep 2
echo "" > nohup.out
echo "Restarting FastAPI server"
else
echo "No such process. Starting new FastAPI server"
fi
nohup uvicorn main:app &
#uvicorn main:app --reload --reload-dir temp
