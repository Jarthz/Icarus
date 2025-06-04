Tables = {
    "Airports":  """
        Airport_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        AirportCode TEXT NOT NULL UNIQUE,
        AirportName TEXT NOT NULL,
        AirportCountry TEXT NOT NULL,
        Runways INTEGER NOT NULL
                 """,
    "Pilots": """
        Pilot_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            LicenseNumber TEXT UNIQUE NOT NULL,
            LicenseCountry TEXT NOT NULL,
            ExperienceYears INTEGER NOT NULL,
            Rank TEXT NOT NULL,
            Email TEXT
        """,
    "Flights": """
        FlightID INTEGER PRIMARY KEY AUTOINCREMENT,
        DepatureDate TEXT,
        Origin TEXT NOT NULL,
        Destination TEXT NOT NULL,
        PilotID INTEGER,
        DepartureTime TEXT NOT NULL,
        ArrivalTime TEXT,
        Status TEXT NOT NULL,
        FOREIGN KEY (Origin) REFERENCES Airports (AirportCode),
        FOREIGN KEY (Destination) REFERENCES Airports (AirportCode),
        FOREIGN KEY (PilotID) REFERENCES Pilots (PilotID)
    """,
    "RouteTimes": """
        Origin TEXT NOT NULL,
        Destination TEXT NOT NULL,
        AverageJourneyTime INTEGER NOT NULL,
        PRIMARY KEY (Origin, Destination),
        FOREIGN KEY (Origin) REFERENCES Airports (AirportCode),
        FOREIGN KEY (Destination) REFERENCES Airports (AirportCode)
    """

}