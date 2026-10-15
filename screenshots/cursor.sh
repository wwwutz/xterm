#!/bin/sh
# park the cursor on a yellow3 "Y" over the default background
printf 'cursor test: \033[33mYy\033[0m\033[2D'
read x
