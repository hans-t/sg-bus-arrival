#! /bin/bash

fab -H $SITENAME \
    -i ~/.ssh/ubuntu-sg.pem \
    deploy