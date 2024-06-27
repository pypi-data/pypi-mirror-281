from cd_http.http import Http
from requests import Session
from fake_useragent import UserAgent as ua

http = Http()
session = Session()
useragent = ua()

