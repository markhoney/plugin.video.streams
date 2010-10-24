#/*
# *   Copyright (C) 2010 Mark Honeychurch
# *
# *
# * This Program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2, or (at your option)
# * any later version.
# *
# * This Program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; see the file COPYING. If not, write to
# * the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# * http://www.gnu.org/copyleft/gpl.html
# *
# */

import os, sys, urllib, urllib2, htmllib, string, unicodedata, re, time, urlparse, cgi, md5, sha, xbmcgui, xbmcplugin, xbmcaddon

__addon__ = xbmcaddon.Addon(id = sys.argv[0][9:-1])
localize  = __addon__.getLocalizedString

xbmcplugin.setPluginCategory(int(sys.argv[1]), 'CCTV')

def message(message, title = "Warning"): #Show an on-screen message (useful for debugging)
 dialog = xbmcgui.Dialog()
 if message:
  if message <> "":
   dialog.ok(title, message)
  else:
   dialog.ok("Message", "Empty message text")
 else:
  dialog.ok("Message", "No message text")

def defaultinfo(folder = 0): #Set the default info for folders (1) and videos (0). Most options have been hashed out as they don't show up in the list and are grabbed from the media by the player
 info = dict()
 if folder:
  info["Icon"] = "DefaultFolder.png"
 else:
  info["Icon"] = "DefaultVideo.png"
 info["Thumb"] = ""
 return info

def checkdict(info, items): #Check that all of the list "items" are in the dictionary "info"
 for item in items:
  if info.get(item, "##unlikelyphrase##") == "##unlikelyphrase##":
   sys.stderr.write("Dictionary missing item: %s" % (item))
   return 0
 return 1

def addlistitem(info, total = 0, folder = 0): #Add a list item (media file or folder) to the XBMC page
 if checkdict(info, ("Title", "Icon", "Thumb", "FileName")):
  liz = xbmcgui.ListItem(info["Title"], iconImage = info["Icon"], thumbnailImage = info["Thumb"])
  liz.setProperty('fanart_image', os.path.join(sys.path[0], 'fanart.jpg'))
  liz.setInfo(type = "Video", infoLabels = info)
  if not folder:
   liz.setProperty("IsPlayable", "true")
  xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = info["FileName"], listitem = liz, isFolder = folder, totalItems = total)


def listcameras():
 info = defaultinfo()
 for i in range(1, 8):
  number = str(i)
  if __addon__.getSetting('stream' + number) == 'true' and __addon__.getSetting('name' + number) <> '' and __addon__.getSetting('string' + number) <> '':
   info["Title"] = __addon__.getSetting('name' + number)
   info["FileName"] = __addon__.getSetting('string' + number)
   addlistitem(info, 0, 0)   
 if __addon__.getSetting('number') > 0:
  total = int(__addon__.getSetting('number'))
  for i in range(1, total + 1):
   info["Title"] = "%s%s" % (__addon__.getSetting('prefix'), str(i))
   info["FileName"] = "%s://%s:%s" % (__addon__.getSetting('proto'), __addon__.getSetting('server'), str(int(__addon__.getSetting('port')) + i - 1))
   addlistitem(info, total, 0)
 

listcameras()
xbmcplugin.addSortMethod(handle = int(sys.argv[1]), sortMethod = xbmcplugin.SORT_METHOD_UNSORTED)
xbmcplugin.addSortMethod(handle = int(sys.argv[1]), sortMethod = xbmcplugin.SORT_METHOD_LABEL)
xbmcplugin.endOfDirectory(int(sys.argv[1]))