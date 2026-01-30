#!/bin/bash
git add .
git commit -m "${1:-'chore: Manual archive update'}"
git push origin main

