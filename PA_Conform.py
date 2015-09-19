#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'mac'

import os
import re
import collections

import AScan.AScan as AScan
import PA_Timecode.PA_Timecode as PA_Timecode

CONFORM_TC = 0x0001
CONFORM_REEL = 0x0010
CONFORM_FILENAME = 0x0010


class PA_Conform(object):
    def __init__(self):
        super(PA_Conform, self).__init__()
        self.matchlist = []

    def run(self, path):
        aa = AScan.AScan()
        ttlist = aa.scanFolder(path, metadata=True)
        print(ttlist)

        # for index, item in enumerate(ttlist):
        #     print aa._getMetadata(item['filename'], item['frames'], allframe=True)

    def saveCSVString(self):
        for matchindex, matchitem in enumerate(self.matchlist):
            csvstring = ''
            for matchrawindex, matchrawitem in enumerate(matchitem[str(matchindex)]):
                csvstring += self.rawmeta._getMetadata(self.rawlist[matchrawitem]['filename'],
                                                       matchitem['matchedframes'][matchrawindex],
                                                       allframe=True)

            # print(matchindex,csvstring)

            if len(csvstring) > 0:
                savepath = os.path.dirname(self.transcodelist[matchindex]['filename'])
                savepath = os.path.join(savepath, 'raw_metadata.csv')
                # print(savepath)
                with open(savepath, 'w') as csvfile:
                    csvfile.write(csvstring)

    def conformFromRAW(self, transcodefiles, rawfiles, keywordrange=(0, 9), checkTC=False):
        self.transcodemeta = AScan.AScan()
        self.transcodelist = self.transcodemeta.scanFolder(transcodefiles, typeFilter=('.dpx', '.exr', '.tif', '.jpg'),
                                                           metadata=True)
        self.rawmeta = AScan.AScan()
        self.rawlist = self.rawmeta.scanFolder(rawfiles, typeFilter=('.ari', '.r3d', '.mov', '.mp4', '.mxf', '.dng'),
                                               metadata=True)

        # print(self.transcodelist)
        # print(self.rawlist)

        startkey = keywordrange[0]
        endkey = keywordrange[-1]

        for transindex, transitem in enumerate(self.transcodelist):
            matchpair = collections.defaultdict(list)
            for rawindex, rawitem in enumerate(self.rawlist):
                if len(os.path.basename(rawitem['filename'])) > endkey:
                    keyword = os.path.basename(rawitem['filename'])[startkey:endkey]
                    if keyword in os.path.basename(transitem['filename']):
                        matchpair[str(transindex)].append(rawindex)
                        matchpair[transitem['filename']].append(rawitem['filename'])

                        if checkTC:
                            tc = PA_Timecode.PA_Timecode()
                            indexoffset = tc.timecodetoframe(tc.timecodesub(transitem['startTimeCode'],
                                                                            rawitem['startTimeCode'], 24),
                                                             24)
                            realstartindex = rawitem['frames'][0] + indexoffset
                            readendindex = realstartindex + transitem['frames'][-1] - transitem['frames'][0] + 1
                            matchpair['matchedframes'].append(
                                [x for x in range(realstartindex, readendindex) if x in rawitem['frames']])

            self.matchlist.append(matchpair)

        return self.matchlist


if __name__ == '__main__':
    testclass = PA_Conform()
    # testclass.run(r'/Volumes/work/TEST_Footage/IOTOVFX_WORKFLOW/To_VFX/20150915')
    # testclass.run(r'/Volumes/work/TEST_Footage/IOTOVFX_WORKFLOW/Conform')
    match = testclass.conformFromRAW(r'/Volumes/work/TEST_Footage/IOTOVFX_WORKFLOW/To_VFX/20150915',
                                     r'/Volumes/work/TEST_Footage/IOTOVFX_WORKFLOW/Conform', checkTC=True)
    print(match)
    testclass.saveCSVString()
