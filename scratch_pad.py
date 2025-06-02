"""
CREATE TABLE Pilots (
    Pilot_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    LicenseNumber TEXT UNIQUE NOT NULL,
    LicenseCountry TEXT NOT NULL,
    ExperienceYears INTEGER NOT NULL,
    Rank TEXT NOT NULL,
    Email TEXT,
    PhoneNumber TEXT
);

airports

CREATE TABLE Airports (
    Airport_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    AirportCode TEXT NOT NULL UNIQUE,        -- e.g. LAX, JFK
    AirportName TEXT NOT NULL,               -- Full airport name
    AirportCountry TEXT NOT NULL,            -- Country name
    Runways INTEGER NOT NULL                 -- Number of runways
);


"""