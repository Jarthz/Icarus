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
);

airports

CREATE TABLE Airports (
    Airport_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    AirportCode TEXT NOT NULL UNIQUE,
    AirportName TEXT NOT NULL,
    AirportCountry TEXT NOT NULL,
    Runways INTEGER NOT NULL
);


"""