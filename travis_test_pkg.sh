#!/bin/bash

cp -r examples/$MODULE $HOME/
cd $HOME/$MODULE
git init
git add .
git commit -m "init"
git tag -a v0.0.1 -m "one"
