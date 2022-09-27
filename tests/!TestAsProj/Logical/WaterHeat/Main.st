(*
OpcUaUnitTesting Example Automation Studio project - WaterHeat task.
This task mimics a water heater to provide more advanced testing.

Author: Marcus Mangel (marcus.mangel@br-automation.com)
Date: 27 September 2022
*)

PROGRAM _INIT
    // Initial values
    WaterTemperature := BASE_TEMPERATURE;
    WaterLevel := 0.0;
    
    HeatRate := 1.0;
    CoolRate := 0.5;
    FillRate := 1.0;
    DrainRate := 1.0;
	 
END_PROGRAM

PROGRAM _CYCLIC
    (*
    This task simulates a water heater which can fill with water and drain water.
    The water inside can also be heated, or cooled to the air if the heater is off.
    
    The water level will never fall below the MIN_LEVEL constant, nor will it fill above
    the MAX_LEVEL constant. Likewise, it will never heat above the MAX_TEMPERATURE constant and
    it won't cool below the BASE_TEMPERATURE constant.
    
    Turning the heater on will cause the water to heat at HeatRate. Turning off the heater 
    will cause it to cool at CoolRate.
    
    Opening the fill valve will cause the water to fill at FillRate. Opening the drain
    valve will cause the water to drain at DrainRate. If the fill valve and the drain valve
    are both closed, the water level will not change.
    
    Rates of change are assumed to be "per second". Therefore, the CYCLES_PER_SECOND constant
    must be consistent with this task's task class cycle time.
    *)
    
	// Heating
    IF HeaterOn THEN
        WaterTemperature := WaterTemperature + (HeatRate/CYCLES_PER_SECOND);
    ELSE
        WaterTemperature := WaterTemperature - (CoolRate/CYCLES_PER_SECOND);
    END_IF;
    
    IF WaterTemperature > MAX_TEMPERATURE THEN
        WaterTemperature := MAX_TEMPERATURE;
    ELSIF WaterTemperature < BASE_TEMPERATURE THEN
        WaterTemperature := BASE_TEMPERATURE;
    END_IF;
    
    // Filling and Draining
    IF FillValveOpen THEN
        WaterLevel := WaterLevel + (FillRate/CYCLES_PER_SECOND);
    END_IF;
    
    IF DrainValveOpen THEN
        WaterLevel := WaterLevel - (DrainRate/CYCLES_PER_SECOND);
    END_IF;
    
    IF WaterLevel > MAX_LEVEL THEN
        WaterLevel := MAX_LEVEL;
        FillValveOpen := FALSE;
    ELSIF WaterLevel < MIN_LEVEL THEN
        WaterLevel := MIN_LEVEL;
        DrainValveOpen := FALSE;
    END_IF;
	 
END_PROGRAM