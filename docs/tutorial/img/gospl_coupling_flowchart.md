# GoSPL Coupling Flowchart

This diagram shows the initialization and execution flow of the DynEarthSol-GoSPL coupling.

## Initialization Flow (in `dynearthsol.cxx`)

```mermaid
flowchart TD
    subgraph INIT["Initialization Phase"]
        A["Start: surface_process_option == 11"] --> B["Create GoSPLDriver instance"]
        B --> C["init_python()"]
        C --> D{Python init OK?}
        D -->|No| E["Delete driver, exit with error"]
        D -->|Yes| F{Is Restart?}
        
        F -->|Yes| G{Mesh file exists?}
        G -->|Yes| H["Reuse existing gospl_mesh.npz"]
        G -->|No| I["Generate new mesh"]
        
        F -->|No| I
        I --> J["Extract surface nodes (BOUNDZ1)"]
        J --> K["generate_mesh(x_coords, y_coords, ...)"]
        
        H --> L["initialize(config_file)"]
        K --> L
        
        L --> M{Initialize OK?}
        M -->|No| N["Delete driver, exit with error"]
        M -->|Yes| O["set_verbose(false)"]
        O --> P["Set coupling_frequency"]
        P --> Q["Initialization Complete ✓"]
    end
```

## Execution Flow (in `bc.cxx::use_gospl`)

```mermaid
flowchart TD
    subgraph EXEC["Coupling Execution Each Step"]
        A1["surface_processes() called"] --> B1{GoSPL driver initialized?}
        B1 -->|No| C1["Return (skip)"]
        B1 -->|Yes| D1["Calculate dt_years"]
        
        D1 --> E1["Accumulate: accumulated_dt += dt"]
        E1 --> F1["Increment: step_counter++"]
        
        F1 --> G1{step_counter < coupling_frequency?}
        G1 -->|Yes| H1["Return early (skip coupling)"]
        G1 -->|No| I1["Reset counters"]
        
        I1 --> J1["Extract surface node coords"]
    end

    subgraph COUPLE["Coupling Steps"]
        J1 --> K1["Step 1: Apply DES elevation to GoSPL\n(apply_elevation_data)"]
        K1 --> L1["Step 2: Get GoSPL elevation BEFORE\n(interpolate_elevation_to_points)"]
        L1 --> M1["Step 3: Run GoSPL erosion\n(run_processes_for_dt)"]
        M1 --> N1["Step 4: Get GoSPL elevation AFTER\n(interpolate_elevation_to_points)"]
        N1 --> O1["Step 5: Compute erosion\n= after - before"]
    end

    subgraph APPLY["Apply Changes"]
        O1 --> P1{Node in bounds?}
        P1 -->|No| Q1["Skip node"]
        P1 -->|Yes| R1["Apply erosion to DES:\ncoord[z] += erosion"]
        Q1 --> S1["Next node"]
        R1 --> S1
        S1 --> T1{More nodes?}
        T1 -->|Yes| P1
        T1 -->|No| U1["Log statistics"]
        U1 --> V1["Done ✓"]
    end
```

## Complete Data Flow

```mermaid
flowchart LR
    subgraph DES["DynEarthSol"]
        D1["Surface Node Coords"]
        D2["Surface Elevations"]
        D3["Updated Topography"]
    end
    
    subgraph GOSPL["GoSPL (LEM)"]
        G1["Mesh (gospl_mesh.npz)"]
        G2["Erosion Processes"]
        G3["Elevation Changes"]
    end
    
    D1 --> |"Extract coords"| G1
    D2 --> |"apply_elevation_data"| G2
    G2 --> |"run_processes_for_dt"| G3
    G3 --> |"interpolate & diff"| D3
```

## Key Components

| Component | File | Purpose |
|-----------|------|---------|
| `GoSPLDriver` | [gospl-driver.cxx](file:///home/echoi2/opt/DynEarthSol/gospl_driver/gospl-driver.cxx) | C++ wrapper for GoSPL Python interface |
| Initialization | [dynearthsol.cxx:547-616](file:///home/echoi2/opt/DynEarthSol/dynearthsol.cxx#L547-L616) | GoSPL driver setup in main() |
| Coupling Logic | [bc.cxx:1589-1719](file:///home/echoi2/opt/DynEarthSol/bc.cxx#L1589-L1719) | `use_gospl()` function for each step |
| Cleanup | [dynearthsol.cxx:910-916](file:///home/echoi2/opt/DynEarthSol/dynearthsol.cxx#L910-L916) | Driver deletion at simulation end |
