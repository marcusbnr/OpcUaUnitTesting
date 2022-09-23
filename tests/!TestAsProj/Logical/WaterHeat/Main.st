
PROGRAM _INIT
    // Initial values
    WaterTemperature := BASE_TEMPERATURE;
    WaterLevel := 0.0;
    
    HeatRate := 0.3;
    CoolRate := 0.1;
    FillRate := 1.0;
    DrainRate := 1.0;
	 
END_PROGRAM

PROGRAM _CYCLIC
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

