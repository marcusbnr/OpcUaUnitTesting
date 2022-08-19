
TYPE
	VisInfo_type : 	STRUCT 
		IpAddr : STRING[80];
		NumConnectedClients : USINT;
		IsItFriday : STRING[10];
	END_STRUCT;
	InfoRefreshState_enum : 
		(
		INFO_REFRESH_STATE_WAIT,
		INFO_REFRESH_STATE_GET_IP,
		INFO_REFRESH_STATE_GET_DAY,
		INFO_REFRESH_STATE_ERROR
		);
END_TYPE
