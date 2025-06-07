class Schema:
    Tables = {
        "Airports":  """
            AirportID INTEGER PRIMARY KEY AUTOINCREMENT,
            AirportCode TEXT NOT NULL UNIQUE,
            AirportName TEXT NOT NULL,
            AirportCountry TEXT NOT NULL,
            Runways INTEGER NOT NULL
        """,
        "Pilots": """
            PilotID INTEGER PRIMARY KEY AUTOINCREMENT,
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
            DepartureDate TEXT,
            Origin INTEGER NOT NULL,
            Destination INTEGER NOT NULL,
            PilotID INTEGER,
            DepartureTime TEXT NOT NULL, -- ISO 8601 format: 'HH:MM'
            ArrivalTime TEXT, -- ISO 8601 format: 'HH:MM'
            Status TEXT NOT NULL DEFAULT 'Scheduled',
            FOREIGN KEY (Origin) REFERENCES Airports (AirportID),
            FOREIGN KEY (Destination) REFERENCES Airports (AirportID),
            FOREIGN KEY (PilotID) REFERENCES Pilots (PilotID)
        """,
        "RouteTimes": """
            Origin INTEGER NOT NULL,
            Destination INTEGER NOT NULL,
            AverageJourneyTime INTEGER NOT NULL,
            PRIMARY KEY (Origin, Destination),
            FOREIGN KEY (Origin) REFERENCES Airports (AirportID),
            FOREIGN KEY (Destination) REFERENCES Airports (AirportID)
        """
    }

    @staticmethod
    def get_auto_increment(table):
        auto_increment_cols = []
        schema = Schema.Tables.get(table)
        if schema:
            lines = schema.strip().splitlines()
            for line in lines:
                line_clean = line.strip().rstrip(',')
                if 'AUTOINCREMENT' in line_clean.upper() and 'PRIMARY KEY' in line_clean.upper():
                    column_name = line_clean.split()[0]
                    auto_increment_cols.append(column_name)
        return auto_increment_cols