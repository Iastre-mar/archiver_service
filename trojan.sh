#!/bin/bash
sudo cp ./archiver.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl enable archiver.service && sudo systemctl start test.service