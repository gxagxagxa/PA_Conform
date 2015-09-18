#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'mac'


import os
import re
import collections

import AScan.AScan as AScan

CONFORM_TC = 0x0001
CONFORM_REEL = 0x0010
CONFORM_FILENAME = 0x0010

class PA_Conform(object):
    def __init__(self):
        super(PA_Conform, self).__init__()
        self.matchlist = []

    def run(self,path):
        aa = AScan.AScan()
        aa.scanFolder(path, metadata=True)
        print(aa.humanFormat())

    def conformFromRAW(self, transcodefiles, rawfiles, keywordrange=(0,9), checkTC=False):
        transcodemeta = AScan.AScan()
        transcodelist = transcodemeta.scanFolder(transcodefiles, typeFilter=('.dpx', '.exr', '.tif', '.jpg'), metadata=True)
        rawmeta = AScan.AScan()
        rawlist = rawmeta.scanFolder(rawfiles, typeFilter=('.ari', '.r3d', '.mov', '.mp4', '.mxf', '.dng'), metadata=True)

        startkey = keywordrange[0]
        endkey = keywordrange[-1]


        for transindex, transitem in enumerate(transcodelist):
            matchpair = collections.defaultdict(list)
            for rawindex, rawitem in enumerate(rawlist):
                if len(os.path.basename(rawitem['filename'])) > endkey:
                    keyword = os.path.basename(rawitem['filename'])[startkey:endkey]
                    if keyword in os.path.basename(transitem['filename']):
                        matchpair[str(transindex)].append(rawindex)
                        matchpair[transitem['filename']].append(rawitem['filename'])

            self.matchlist.append(matchpair)

        return self.matchlist





if __name__ == '__main__':
    testclass = PA_Conform()
    # testclass.run(r'/Volumes/work/TEST_Footage/IOTOVFX_WORKFLOW')
    match = testclass.conformFromRAW(r'/Volumes/work/TEST_Footage/IOTOVFX_WORKFLOW/To_VFX/20150915',
                             r'/Volumes/work/TEST_Footage/IOTOVFX_WORKFLOW/Conform')
    print(match)