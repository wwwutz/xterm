#!/bin/sh
e() { printf "%-14s \033[%sm  2 - console.log(\"Hello\")  \033[0m\n" "$1" "$2"; }
e "plain" ""
e "fg1" "31"; e "fg2" "32"; e "fg9" "91"; e "fg10" "92"
e "bg1" "41"; e "bg2" "42"; e "bg9" "101"; e "bg10" "102"; e "bg7" "47"; e "bg0" "40"
e "fg0 bg1" "30;41"; e "fg0 bg2" "30;42"; e "fg7 bg0" "37;40"; e "fg15 bg0" "97;40"
e "fg0 deflt bg" "30"; e "fg7 deflt bg" "37"; e "fg15" "97"
e "inverse" "7"; e "inv fg1" "7;31"; e "inv bg2" "7;42"; e "inv fg0" "7;30"
e "faint" "2"; e "faint fg1" "2;31"; e "faint bg1" "2;41"; e "faint fg0" "2;30"
e "dim+bg9 fg0" "2;30;101"
e "HIDE same idx" "38;5;4;48;5;4"; e "HIDE same tc" "38;2;9;80;9;48;2;9;80;9"; e "HIDE conceal" "8"
read x
