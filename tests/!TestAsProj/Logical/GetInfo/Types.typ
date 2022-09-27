(*
OpcUaUnitTesting Example Automation Studio project - GetInfo task datatypes

Author: Marcus Mangel (marcus.mangel@br-automation.com)
Date: 27 September 2022
*)

TYPE
	VisInfo_type : 	STRUCT  (*Contains all information shown on the HMI*)
		IpAddr : STRING[80]; (*PLC's IP Address*)
		IsItFriday : STRING[10]; (*String showing the answer to the question "Is it Friday yet?"*)
	END_STRUCT;
	InfoRefreshState_enum : 
		( (*State machine states*)
		INFO_REFRESH_STATE_WAIT, (*Wait for a command*)
		INFO_REFRESH_STATE_GET_IP, (*Get the PLC's IP Address*)
		INFO_REFRESH_STATE_GET_DAY, (*Figure out if today is Friday*)
		INFO_REFRESH_STATE_ERROR (*Error refreshing information*)
		);
END_TYPE
