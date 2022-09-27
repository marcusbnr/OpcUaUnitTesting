(*
OpcUaUnitTesting Example Automation Studio project - Global datatypes

Author: Marcus Mangel (marcus.mangel@br-automation.com)
Date: 27 September 2022
*)
TYPE
	GlobalTestStruct : 	STRUCT  (*Testing using a basic structure*)
		TestUDINT : UDINT; (*Testing with Unsigned Double Integer*)
		TestBOOL : BOOL; (*Testing with Boolean*)
		TestSTRING : STRING[50]; (*Testing with String*)
		TestSubStruct : GlobalTestSubStruct; (*Testing using a structure in a structure (structure-ception)*)
	END_STRUCT;
	GlobalTestSubStruct : 	STRUCT  (*Testing using a structure in a structure (structure-ception)*)
		TestREAL : REAL; (*Testing with REAL*)
		TestLREAL : LREAL; (*Testing with Long REAL*)
	END_STRUCT;
END_TYPE
