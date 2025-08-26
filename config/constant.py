"""
Some constants related to Fudan University's network authentication.
"""

# 用户自定义配置的存储位置
USER_SETTING_PATH = r"./config/user.py"

# The timeout period for a single request. Unit: seconds.
TIMEOUT = 10

BASE_URL  = "http://10.102.250.36"
LOGIN_URL = f"{BASE_URL}/#/login" # http://10.102.250.36/#/login

API_URL = f"{BASE_URL}/api" # http://10.102.250.36/api
IP_V1_API_URL = f"{API_URL}/v1/ip" # http://10.102.250.36/api/v1/ip
IP_API_URL = IP_V1_API_URL # the default ip api
PRE_LOGIN_V1_API_URL = f"{API_URL}/v1/pre_login"
PRE_LOGIN_API_URL = PRE_LOGIN_V1_API_URL # the default pre_login api
LOGIN_V1_API_URL = f"{API_URL}/v1/login" # http://10.102.250.36/api/v1/login
LOGIN_API_URL = LOGIN_V1_API_URL # the default login api

ERROR_FEATURES = {
	"获取会话信息失败，请连接正确的网络后重新认证。Failed to get session information, please connect to the correct network and re-authentication.": "不在复旦寝室网覆盖范围内",
}

REQUIRED_MODULES = {
	"requests": "requests",
}