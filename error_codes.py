#!/usr/bin/python

def error_report(error_code):
  if (error_code == "webdriver"):
    return "Webdriver error. Unable to open browser instance." 
  
  if (error_code == "up"):
    return "Username/Password error. Unable to log in." 
  
  if (error_code == "login-button"):
    return "Unable to press 'Login' button." 
  
  if (error_code == "capture-button"):
    return "Unable to press 'Capture' button."

  if (error_code == "ssh"):
    return "'ssh' command failed." 

  if (error_code == "scp"):
    return "'scp' command failed." 
  
