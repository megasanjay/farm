#!/usr/bin/python
from subprocess import Popen, PIPE
from selenium import webdriver
import shlex
import logging
import time
import sys
import error_codes
from addresses import *

logging.basicConfig(filename = log_file_name, level = logging.DEBUG)

while (True):
  for ip_address_value in ip_addresses_list:
    colon_position = ip_address_value.find(':')
    ip_address = ip_address_value[:colon_position + 1]
    port = ip_address_value[colon_position:]
    
    error_flag = False
    
    print(">> Opening browser...\n")
    try:
      driver = webdriver.Chrome('./chromedriver74.exe')
      driver.get("http://" + ip_address_value + "/login/")
    except:
      error_message = error_report("webdriver") + " - " + sys.exc_info()[0]
      logging.critical(error_message)
      error_flag = True

    print(">> Inputting credentials...\n")
    try:
      username = driver.find_element_by_id("login_input_username")
      password = driver.find_element_by_id("login_input_password")
      username.send_keys("user")
      password.send_keys("user")
    except:
      error_message = error_report("up") + " - " + sys.exc_info()[0]
      logging.critical(error_message)
      error_flag = True
    
    print(">> Waiting for " + str(time_to_sleep_between_button_presses) + " seconds...\n")
    time.sleep(time_to_sleep_between_button_presses)

    print(">> Pressing 'Login' button...\n")
    try:
      driver.find_element_by_id("button-login").click()
      print(">> Login successful...\n")
    except:
      error_message = error_report("login-button") + " - " + sys.exc_info()[0]
      logging.critical(error_message)
      error_flag = True

    print(">> Waiting for " + str(time_to_sleep_between_button_presses) + " seconds...\n")
    time.sleep(time_to_sleep_between_button_presses)
      
    print(">> Pressing 'Capture' button...\n")
    try:
      driver.find_element_by_id('button-save-image').click()
      print(">> Capture successful...\n")
      logging.info("Image capture for " + ip_address_value + " successful...")
    except:
      error_message = error_report("capture-button") + " - " + sys.exc_info()[0]
      logging.critical(error_message)
      error_flag = True
    
    print(">> Closing browser...\n")
    driver.quit()

    if (error_flag == True):
      print("Error ", sys.exc_info()[0] , " occured.")
      print("Check log file for details")
      print()

  for ssh_address_value in ssh_addresses_list:
    colon_position = ssh_address_value.find(':')
    ssh_address = ssh_address_value[:colon_position ]
    port = ssh_address_value[colon_position + 1:]

    error_flag = False

    command_line = "ssh -t fliruser@" + ssh_address + " -p " + port + " 'rm -r images"
    command_line = command_line + " && mkdir images && cp /FLIR/images/* ./images'"
    logging.info("Running command '" + command_line + "'")
    print(">> Running '" + command_line + "'...\n")

    try:
      args = shlex.split(command_line)
      p1 = Popen(args, stdout = PIPE, stderr = PIPE)
      stdout,stderr = p1.communicate()
      logging.info("ssh command for " + ssh_address_value + " successful...")
    except:
      error_message = error_report("ssh") + " - " + sys.exc_info()[0]
      logging.critical(error_message)
      error_flag = True
    
    command_line = "scp -P " + port + " -r fliruser@" + ssh_address + ":images " + storage_folder
    logging.info("Running command '" + command_line + "'")
    print(">> Running '" + command_line + "'...\n")

    try:
      args = shlex.split(command_line)
      p2 = Popen(args, stdout = PIPE, stderr = PIPE)
      stdout,stderr = p2.communicate()
      logging.info("scp command for " + ssh_address_value + " successful...")
    except:
      error_message = error_report("scp") + " - " + sys.exc_info()[0]
      logging.critical(error_message)
      error_flag = True

    if (error_flag == True):
      print("Error ", sys.exc_info()[0] , " occured.")
      print("Check log file for details")
      print()
  print(">> Waiting for " + str(time_to_sleep_between_captures) + " seconds...\n")      
  time.sleep(time_to_sleep_between_captures)