#!/usr/bin/env python
# -*- encoding: utf-8 -*-
__author__ = 'mac'

class PA_Timecode(object):
    def __init__(self):
        super(PA_Timecode, self).__init__()

    def timecodetoframe(self, timecode, fps):
        # print('==== __timecodetoframe  ====')
        ffps = float(fps)
        hh = int(timecode[0:2])
        mm = int(timecode[3:5])
        ss = int(timecode[6:8])
        ff = 0
        if timecode[8:9] == '.':
            ff = int(float(timecode[9:11]) / 100.0 * ffps)
        else:
            ff = int(timecode[9:11])
        # print(ffps, hh, mm, ss, ff)
        framecount = int((hh * 3600 * ffps) + int(mm * 60 * ffps) + int(ss * ffps) + ff)
        # print(framecount)
        return framecount

    def frametotimecode(self, frame, fps, type='normal'):
        # print('==== __frametotimecode  ====')
        ffps = float(fps)
        fframe = int(frame)
        hh = fframe // int(3600 * ffps)
        fframe = fframe - int(hh * 3600 * ffps)
        mm = fframe // int(60 * ffps)
        fframe = fframe - int(mm * 60 * ffps)
        ss = fframe // ffps
        ff = fframe - ss * ffps
        if type == 'normal':
            tcstring = '%02d:%02d:%02d:%02d' % (hh, mm, ss, ff)
        if type == 'ms':
            tcstring = '%02d:%02d:%02d.%03d' % (hh, mm, ss, int(ff/ffps))
        # print(tcstring)
        return tcstring

    def timecodeadd(self, tc1, tc2, fps):
        # print('==== __timecodeadd  ====')
        frame1 = self.timecodetoframe(tc1, fps)
        frame2 = self.timecodetoframe(tc2, fps)
        # print(frame1, frame2)
        frame2 = frame1 + frame2
        return self.frametotimecode(frame2, fps)

    def timecodesub(self, tc1, tc2, fps):
        # print('==== __timecodeadd  ====')
        frame1 = self.timecodetoframe(tc1, fps)
        frame2 = self.timecodetoframe(tc2, fps)
        # print(frame1, frame2)
        frame2 = frame1 - frame2
        if frame2 < 0:
            return '-1:-1:-1:-1'
        return self.frametotimecode(frame2, fps)