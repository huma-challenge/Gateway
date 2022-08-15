#!/bin/bash

echo "Clone proto files from repo ... "
rm -rf ./protobufs
git clone https://github.com/huma-challenge/protobufs.git

echo "Compile proto file to python ... "
python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ ./protobufs/account_manager/account.proto

echo "Makemigrations and apply migrates ... "
python3 manage.py makemigrations --noinput 
python3 manage.py migrate --noinput 

echo "Collect static files ..."
python3 manage.py collectstatic --noinput 


echo "Run gunicorn development server ... "
gunicorn -b 0.0.0.0:8000 --workers 1 config.wsgi:application 

