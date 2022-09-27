(*
OpcUaUnitTesting Example Automation Studio project - GetInfo task.
This task populates the ContentInfo content of the mappView HMI

Author: Marcus Mangel (marcus.mangel@br-automation.com)
Date: 27 September 2022
*)

PROGRAM _INIT
    CmdRefreshInfo := TRUE; // Refresh all information on startup
	 
END_PROGRAM

PROGRAM _CYCLIC
    // Refresh Info state machine
    CASE InfoRefreshState OF
        INFO_REFRESH_STATE_WAIT: // Wait for a command
            IF CmdRefreshInfo THEN
                CmdRefreshInfo := FALSE;
                InfoRefreshState := INFO_REFRESH_STATE_GET_IP;
            END_IF;
            
        INFO_REFRESH_STATE_GET_IP: // Get the PLC's IP Address
            fb_CfgGetIpAddr.enable := TRUE;
            fb_CfgGetIpAddr.pDevice := ADR('IF3');
            fb_CfgGetIpAddr.pIPAddr := ADR(VisInfo.IpAddr);
            fb_CfgGetIpAddr.Len := SIZEOF(VisInfo.IpAddr);
            
            IF (fb_CfgGetIpAddr.status <> ERR_FUB_BUSY) AND (fb_CfgGetIpAddr.status <> ERR_FUB_ENABLE_FALSE) THEN
                IF fb_CfgGetIpAddr.status = ERR_OK THEN
                    fb_CfgGetIpAddr.enable := FALSE;
                    InfoRefreshState := INFO_REFRESH_STATE_GET_DAY;
                ELSE
                    Error := TRUE;
                    InfoRefreshState := INFO_REFRESH_STATE_ERROR;
                END_IF;
            END_IF;
            
        INFO_REFRESH_STATE_GET_DAY: // Figure out if it's Friday
            brsmemset(ADR(VisInfo.IsItFriday), 0, SIZEOF(VisInfo.IsItFriday));
            brsstrcpy(ADR(VisInfo.IsItFriday), ADR('No :('));
            
            fb_DTStructureGetTime.enable := TRUE;
            fb_DTStructureGetTime.pDTStructure := ADR(DtStruct);
            
            IF (fb_DTStructureGetTime.status <> ERR_FUB_BUSY) AND (fb_DTStructureGetTime.status <> ERR_FUB_ENABLE_FALSE) THEN
                IF fb_DTStructureGetTime.status = ERR_OK THEN
                    fb_DTStructureGetTime.enable := FALSE;
                    IF DtStruct.wday = 5 THEN
                        brsmemset(ADR(VisInfo.IsItFriday), 0, SIZEOF(VisInfo.IsItFriday));
                        brsstrcpy(ADR(VisInfo.IsItFriday), ADR('Yes!'));
                    END_IF;
                    InfoRefreshState := INFO_REFRESH_STATE_WAIT;
                ELSE
                    Error := TRUE;
                    InfoRefreshState := INFO_REFRESH_STATE_ERROR;
                END_IF;
            END_IF;
                                                      
            
        INFO_REFRESH_STATE_ERROR: // Error getting info
            IF CmdErrorReset THEN
                CmdErrorReset := FALSE;
                Error := FALSE;
                fb_CfgGetIpAddr.enable := FALSE;
                InfoRefreshState := INFO_REFRESH_STATE_WAIT;
            END_IF;
        
    END_CASE;
    
    //Call function blocks
    fb_CfgGetIpAddr();
    fb_DTStructureGetTime();
END_PROGRAM

