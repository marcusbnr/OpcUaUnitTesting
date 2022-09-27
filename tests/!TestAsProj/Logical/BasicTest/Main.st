(*
OpcUaUnitTesting Example Automation Studio project - BasicTest task.
This task provides variables for basic testing.

Author: Marcus Mangel (marcus.mangel@br-automation.com)
Date: 27 September 2022
*)

PROGRAM _INIT
    // Use variables in task so that the compiler includes them
    gGlobalInt;
    gGlobalUInt;
    gGlobalString;
    gTestStruct;
    
    TestBOOL;
    TestDINT;
    TestDT;
    TestTIME;
	 
END_PROGRAM

PROGRAM _CYCLIC
    // Calculator test
	AdditionOut := AdditionIn1 + AdditionIn2;
	 
END_PROGRAM

