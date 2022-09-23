
PROGRAM _INIT
    fb_MpAlarmXCore.MpLink := ADR(gAlarmXCore);
    fb_MpAlarmXCore.Enable := TRUE;
	 
END_PROGRAM

PROGRAM _CYCLIC
	fb_MpAlarmXCore();
	 
END_PROGRAM

PROGRAM _EXIT
	fb_MpAlarmXCore(Enable := FALSE);
	 
END_PROGRAM

