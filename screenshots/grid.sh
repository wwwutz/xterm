#!/bin/sh
# rows: background (default, 0..15); columns: foreground 0..15
printf '      '; i=0; while [ $i -lt 16 ]; do printf '%-4s' $i; i=$((i+1)); done; echo
for bg in def 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do
  printf '%-4s  ' $bg
  [ $bg = def ] || printf '\033[48;5;%dm' $bg
  fg=0; while [ $fg -lt 16 ]; do printf '\033[38;5;%dmAb%d ' $fg $((fg%10)); fg=$((fg+1)); done
  printf '\033[0m\n'
done
printf '\nfaint:  '; for fg in 7 11 14 15; do printf '\033[2;38;5;%dmfaint%d \033[0m' $fg $fg; done
printf '\nconceal: [\033[8mhidden\033[0m]  fg==bg: [\033[38;5;4;48;5;4msame\033[0m]\n'
printf 'truecolor dracula fg f8f8f2: \033[38;2;248;248;242mHello world\033[0m\n'
printf 'grey ramp 237 on 235: \033[38;5;237;48;5;235m comment text \033[0m\n'
