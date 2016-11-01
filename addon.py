# -*- coding: utf-8 -*-
# addon.py
# dnvodPlayer

import xbmcplugin, xbmcgui,urlparse,xbmcaddon
import urllib
import urllib2
import re
import requests
import sys
try:
    from ChineseKeyboard import Keyboard
except:
    from xbmc import Keyboard




addon = xbmcaddon.Addon(id='plugin.video.dnvodPlayer')
__language__ = addon.getLocalizedString
rootDir = addon.getAddonInfo('path')
rootDir = xbmc.translatePath(rootDir)
url1 = 'http://www.dnvod.eu'
url2 = 'http://www.dnvod.eu/Movie/Readyplay.aspx?id=7COqHhPaRZg%3d'
#get ASP.NET_SessionId
def getSessionID (url1,url2):
    s=requests.Session()
    s.get(url1)
    r1 = s.get(url2)
    header = r1.headers
    rrrr = [header]
    reg = r'ASP.NET_SessionId=(.*); path=/; HttpOnly'
    partern =  re.compile(reg)
    sessionID = partern.findall(rrrr[0]['Set-Cookie'])
    return sessionID

def getCookies():
    cookies = 'ASP.NET_SessionId='+sessionID
    return cookies
def getUserAgent():
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    return user_agent

sessionID = getSessionID(url1,url2)[0]
cookies = getCookies()
user_agent = getUserAgent()


#create user headers
headers = {"User-Agent": user_agent,
"Content-Type": "application/x-www-form-urlencoded",
"Accept": "*/*",
"Referer": "http://www.dnvod.eu/Movie/Readyplay.aspx?id=jydSM%2fudfCo%3d",
"Accept-Encoding": "",
"Accept-Language": "de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,zh;q=0.2,zh-TW;q=0.2,fr-FR;q=0.2,fr;q=0.2",
"X-Requested-With": "XMLHttpRequest",
"DNT": "1",
"Cookie": cookies}

#create server headers
headers2 = {"Host": "www.dnvod.eu",
"Content-Length": "36",
"Cache-Control": "nax-age=0",
"Accept": "*/*",
"Origin": "http://www.dnvod.eu",
"X-Requested-With": "XMLHttpRequest",
"User-Agent": user_agent,
"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
"DNT": "1",
"Referer": "http://www.dnvod.eu/Movie/Readyplay.aspx?id=%2bWXev%2bhf16w%3d",
"Accept-Encoding": "",
"Accept-Language": "de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,zh;q=0.2,zh-TW;q=0.2,fr-FR;q=0.2,fr;q=0.2",
"Connection": "keep-alive",
"Cookie": cookies}


plugin_url = sys.argv[0]
handle = int(sys.argv[1])
params = dict(urlparse.parse_qsl(sys.argv[2].lstrip('?')))
searchResult=None
selectmovie=''
isFolder=True
searchResultName=None
detailResult=None
playUrl=''

#main menu
def index():
    listitem=xbmcgui.ListItem("搜索..")
    isFolder=True
    url = plugin_url + '?act=Search&name=search'
    xbmcplugin.addDirectoryItem(handle,url,listitem,isFolder)
    xbmcplugin.endOfDirectory(handle)
    xbmcplugin.endOfDirectory(handle)

#Search menu
def Search():
    kb = Keyboard('',u'请输入想要观看的电影或电视剧名称')
    kb.doModal()
    if not kb.isConfirmed(): return
    sstr = kb.getText()
    if not sstr: return
    inputMovieName=urllib.quote_plus(sstr)
    urlSearch = 'http://www.dnvod.eu/Movie/Search.aspx?tags='+inputMovieName
    searchRequest = urllib2.Request(urlSearch,None,headers)
    searchResponse = urllib2.urlopen(searchRequest)
    searchdataResponse = searchResponse.read()
    searchReg = r'<a href="(.*%3d)">'
    searchPattern = re.compile(searchReg)
    searchResult = searchPattern.findall(searchdataResponse)

    fo = open(rootDir+"/searchResult.txt", "w")
    for node in searchResult:
        fo.write(str(node)+'\n')
    fo.close



    searchRegName = r'3d" title="(.*)">'
    searchPatternName = re.compile(searchRegName)
    searchResultName = searchPatternName.findall(searchdataResponse)

    fo = open(rootDir+"/searchResultName.txt", "w")
    for node in searchResultName:
        fo.write(str(node)+'\n')
    fo.close

    listitem = xbmcgui.ListItem('[COLOR FFFF00FF]当前搜索: [/COLOR][COLOR FFFFFF00]('+sstr+') [/COLOR][COLOR FF00FFFF]共计：'+str(len(searchResult))+'[/COLOR]【[COLOR FF00FF00]'+'点此输入新搜索内容'+'[/COLOR]】')
    url=sys.argv[0]+'?act=Search&name'+inputMovieName
    xbmcplugin.addDirectoryItem(handle, url, listitem, True)
    for i in range(len(searchResultName)):
        listitem = xbmcgui.ListItem(searchResultName[i])
        url=sys.argv[0]+'?act=Searchr&id='+str(i+1)
        xbmcplugin.addDirectoryItem(handle, url, listitem, True)
        print str(i+1)+': '+searchResultName[i]+'\n'
    xbmcplugin.endOfDirectory(handle)

#Detail menu
def Detail():
    whichResultStr = params['id']
    whichResultInt = int(whichResultStr)-1


    fo = open(rootDir+"/searchResult.txt", "r+")
    searchResult = fo.readlines()
    fo.close

    fo = open(rootDir+"/searchResultName.txt", "r+")
    searchResultName = fo.readlines()
    fo.close

    filmIdReg = r'id=(.*%3d)'
    filmIdPattern = re.compile(filmIdReg)
    filmIdResult = filmIdPattern.findall(searchResult[whichResultInt])
    searchUrl = 'http://www.dnvod.eu/Movie/detail.aspx?id='+filmIdResult[0]
    detailRequest = urllib2.Request(searchUrl,None,headers)
    detailResponse = urllib2.urlopen(detailRequest)
    detaildataResponse = detailResponse.read()
    detailReg = r'<div class="bfan-n"><a href="(.*)" target="_blank">.*</a></div>'
    detailPattern = re.compile(detailReg)
    detailResult = detailPattern.findall(detaildataResponse)
    fo = open(rootDir+"/detailResult.txt", "w")
    for node in detailResult:
        fo.write(str(node)+'\n')
    fo.close

    listitem = xbmcgui.ListItem('[COLOR FFFF00FF]当前选择: [/COLOR][COLOR FFFFFF00]('+searchResultName[whichResultInt]+') [/COLOR][COLOR FF00FFFF]共计：'+str(len(detailResult))+'集[/COLOR]【[COLOR FF00FF00]'+'点此输入新搜索内容'+'[/COLOR]】')
    url=sys.argv[0]+sys.argv[2]
    xbmcplugin.addDirectoryItem(handle, url, listitem, True)
    for i in range(len(detailResult)):
        listitem = xbmcgui.ListItem('第'+str(i+1)+'集')
        url=sys.argv[0]+'?act=play&id='+params['id']+'&ep='+str(i+1)
        xbmcplugin.addDirectoryItem(handle, url, listitem, True)
    xbmcplugin.endOfDirectory(handle)


#Episode player
def Episode():

    fo = open(rootDir+"/detailResult.txt", "r+")
    detailResult = fo.readlines()
    fo.close

    fo = open(rootDir+"/searchResultName.txt", "r+")
    searchResultName = fo.readlines()
    fo.close

    whichEpisodeStr = params['ep']
    whichEpisodeInt = int(whichEpisodeStr)-1
    playUrl = 'http://www.dnvod.eu'+detailResult[whichEpisodeInt]
    requestFir = urllib2.Request(playUrl,None,headers)
    responseFir  = urllib2.urlopen(requestFir)
    data_responseFir = responseFir.read()

    reg     = r'id:.*\'(.*)\','
    pattern = re.compile(reg)
    result  = pattern.findall(data_responseFir)
    para2   = result[0]

    urlSec = 'http://www.dnvod.eu/Movie/GetResource.ashx?id='+para2+'&type=htm'

    regkeyString = r'key:.*\'(.*)\','
    patternkeyString = re.compile(regkeyString)
    resultkeyString = patternkeyString.findall(data_responseFir)
    keyString = resultkeyString[0]


    data = urllib.urlencode({'key':keyString})
    requestSec = urllib2.Request(urlSec,data,headers2)
    responseSec = urllib2.urlopen(requestSec)
    real_url = responseSec.read()
    pattern = re.compile(r'(\d||\d\d||\d\d\d||\d\d\d\d||\d\d\d\d\d||\d\d\d\d\d\d||\d\d\d\d\d\d\d||\d\d\d\d\d\d\d\d)\.mp4')
    num = re.split(pattern,real_url)
    hdurl = num[0]+'hd-'+num[1]+'.mp4'+num[2]

    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem=xbmcgui.ListItem(u'播放')
    listitem.setInfo(type='video', infoLabels={"Title": searchResultName[int(params['id'])-1]+' 第'+params['ep']+'集'})
    playlist.add(real_url, listitem=listitem)
    xbmc.Player().play(playlist)

{
    'index': index,
    'Search': Search,
    'Searchr': Detail,
    'play':Episode
}[params.get('act', 'index')]()

