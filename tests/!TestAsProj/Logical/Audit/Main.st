
PROGRAM _INIT
    fb_MpAuditTrail.MpLink := ADR(gAuditTrail);
    fb_MpAuditTrail.Enable := TRUE;
    fb_MpAuditTrail.DeviceName := ADR('FD_Audit');
	 
END_PROGRAM

PROGRAM _CYCLIC
	fb_MpAuditTrail();
	 
END_PROGRAM

PROGRAM _EXIT
	fb_MpAuditTrail(Enable := FALSE);
	 
END_PROGRAM

