from subprocess import Popen, PIPE
import shlex
import sys
command_line = "ssh -t fliruser@206.123.141.137 -p 2002 'rm -r images && mkdir images && cp /FLIR/images/* ./images'"
args = shlex.split(command_line)
p2 = Popen(args, stdout=PIPE,stderr=PIPE)
stdout,stderr = p2.communicate()
command_line = "scp -P 2002 -r fliruser@206.123.141.137:images /mnt/c/Users/sanja/Desktop/senal_project/"
args = shlex.split(command_line)
p3 = Popen(args, stdout=PIPE,stderr=PIPE)
stdout,stderr = p3.communicate()