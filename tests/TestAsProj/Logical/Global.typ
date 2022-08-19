
TYPE
	GlobalTestStruct : 	STRUCT 
		TestUDINT : UDINT;
		TestBOOL : BOOL;
		TestSTRING : STRING[50];
		TestSubStruct : GlobalTestSubStruct;
	END_STRUCT;
	GlobalTestSubStruct : 	STRUCT 
		TestREAL : REAL;
		TestLREAL : LREAL;
	END_STRUCT;
END_TYPE
