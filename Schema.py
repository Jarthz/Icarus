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
            Origin TEXT NOT NULL,
            Destination TEXT NOT NULL,
            PilotID INTEGER,
            DepartureTime TEXT NOT NULL, -- ISO 8601 format: 'HH:MM'
            ArrivalTime TEXT, -- ISO 8601 format: 'HH:MM'
            Status TEXT NOT NULL DEFAULT 'Scheduled',
            FOREIGN KEY (Origin) REFERENCES Airports (AirportCode),
            FOREIGN KEY (Destination) REFERENCES Airports (AirportCode),
            FOREIGN KEY (PilotID) REFERENCES Pilots (PilotID)
        """,
        "RouteTimes": """
            Origin INTEGER NOT NULL,
            Destination INTEGER NOT NULL,
            AverageJourneyTime INTEGER NOT NULL,
            PRIMARY KEY (Origin, Destination),
            FOREIGN KEY (Origin) REFERENCES Airports (AirportID),
            FOREIGN KEY (Destination) REFERENCES Airports (AirportID)
        """,
        "Users": """
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT UNIQUE NOT NULL,
            Password TEXT NOT NULL
        """,
        "AuditLog": """
        LogID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT NOT NULL,
        Action TEXT NOT NULL,
        TableName TEXT, 
        Timestamp TEXT DEFAULT (datetime('now', 'localtime')),
        Details TEXT
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

    """
    for use in the CLI and the logic layer. Data Control by centralisation
    """
    main_menu = {
        1: ["Add new record", "add_record"],
        2: ["Delete record", 'delete'],
        3: ["Search all records", 'search_all'],
        4: ["Search for specific record", 'search'],
        5: ["Update record", 'update'],
        6: ['View Audit Log', 'audit_log'],
        7: ["Exit", 'exit']
    }
