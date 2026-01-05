flowchart TD
    %% Define Styles
    classDef ai fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef db fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef file fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,stroke-dasharray: 5 5;
    classDef term fill:#212121,stroke:#000,stroke-width:2px,color:#fff;

    %% Nodes
    User([User / Data Engineer])
    
    subgraph Phase1 [Phase 1: Logic Generation]
        ChatAI(Chat AI: ChatGPT)
        Prompt[Context-Rich Prompt]
    end

    subgraph Phase2 [Phase 2: Execution Engine]
        SQL[Complex SQL Query\nWindow Functions & Z-Score]
        DB[(PostgreSQL DB\nDocker Container)]
        Export(Data Export Command)
    end

    subgraph Phase3 [Phase 3: Automated Analysis]
        CSV[/anomalies.csv\nRaw Data/]
        CLI_Tool(CLI Analyzer\nPython Script)
        Report[Final Fraud Alert\nNatural Language Summary]
    end

    %% Connections
    User -->|Defines Logic| Prompt
    Prompt --> ChatAI
    ChatAI -->|Generates| SQL
    SQL -->|Executed on| DB
    DB -->|Filters Anomalies| Export
    Export -->|Pipes Output| CSV
    CSV -->|Input Stream| CLI_Tool
    CLI_Tool -->|Detects Outliers| Report

    %% Apply Styles
    class ChatAI,CLI_Tool ai;
    class DB,SQL db;
    class CSV,Report file;
    class Export term;