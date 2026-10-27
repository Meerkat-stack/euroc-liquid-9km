# EuRoC L9 Liquid Rocket Simulation

A Python-based flight simulation and optimization project built with **RocketPy** for the European Rocketry Challenge (**EuRoC**) in the **Liquid 9 km** category.

## Project Structure

```text
euroc-liquid-9km/
│
├── output/                   # Generated reports, KML files, and plots
├── src/                      # Source code modules
│   ├── __init__.py
│   ├── build.py              # Rocket, motor, tank, and parachute constructors
│   ├── config.py             # Parameter budget and configuration constants
│   ├── inertia.py            # Analytical center of mass & inertia calculations
│   ├── optimalization.py     # Fin geometry and payload mass optimization loops
│   ├── report.py             # Flight reports and export utilities
│   └── validation.py         # EuRoC rules verification module
│
├── main.py                   # Main CLI entry point
├── requirements.txt          # Python dependencies
└── README.md
```

## Installation

Ensure you have Python 3.10+ installed, then install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

The simulation is controlled via `main.py` using the `--mode` argument:

1. **Nominal Flight Report (Recommended for final review):**
   ```bash
   python3 main.py --mode nominal
   ```

2. **Standard Baseline Simulation:**
   ```bash
   python3 main.py --mode standard
   ```

3. **Fin Optimization:**
   ```bash
   python3 main.py --mode optimize-fins --live
   ```

4. **Payload Mass Optimization:**
   ```bash
   python3 main.py --mode optimize-mass
   ```
