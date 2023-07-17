# LOCUST SETTINGS
FLASK_IP = "127.0.0.1"
FLASK_PORT = 401
MASTER_IP = "127.0.0.1"     # Interface that is listened by Locust Master
MASTER_PORT = 402           # Default: 402. Port for Locust SLAVES, that will use 2 ports: MASTER_PORT and MASTER_PORT+1
LOG_LEVEL = "INFO"          # Choose between DEBUG/INFO/WARNING/ERROR/CRITICAL

# TEST SETTINGS
SERVER_HOST = "XXX.visonic.com"
SERVER_PORT = "443"
LOGIN = ""
PASS = ""

operator_db = "operators.json"
units_on_page = 50          # possible values: 15, 50, 100, 200
client_number = 100         # Default: 100  -   count of User Operators (for Bratislava: 50)
spawn_rate = 1              # count panels per second by one slave thread
task_period = 1             # in sec, Default: 1.0 => 96 RPS for ./launch.sh
gui_oper_delay = 1          # make hatchrate = 1 to be equivalent to 0.25

# app definitions
DEVICE_MODEL = "SM-G970F"                                   # Samsung Galaxy S10e
DEVICE_SW = "RP1A.200720.012"                               # ANDROID 12 (18.02.2021)
INSTALLER_REST_VERSION = "8.0"                              # INSTALLER REST VERSION. PM 4.8 = 6.0, PM 4.10 = 7.0, PM 4.12 = 8.0
INSTALLER_APP_ID = "12345678-aaaa-cccc-eeee-{}"             # application unique identifier (changed after app reinstall)
INSTALLER_APP_TYPE = ""                                     # Alarm Install APP ID
USER_REST_VERSION = "10.0"                                  # USER REST VERSION. PM 4.6 = 8.0, PM 4.8 = 8.0, PM 4.10 = 9.0, PM 4.12 = 10.0
USER_APP_ID = "abcdef90-0000-0000-0000-{}"                  # application unique identifier (changed after app reinstall)
USER_APP_TYPE = ""                                          # Connect Alarm APP ID
USER_PUSH_TYPE = "ANDROID"                                  # Possible values: "ANDROID" and "IPHONE"
USER_PUSH_TOKEN = "PUSHPUSH-push-push-push-{}"              # ID Format to get random unique ID for panels push
APP_PUSH_VER = 7                                            # APP PUSH VERSION. PM 4.6 = 5|6, PM 4.8 = 5|6, PM 4.10 = 7
APP_PUSH_MODE = 1119                                        # Enable all push statuses
