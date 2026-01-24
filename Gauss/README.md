# Gaussian Batch Calculator with BSSE Correction

A Python-based tool for batch processing Gaussian calculations with BSSE (Basis Set Superposition Error) correction capabilities. This tool automates quantum chemistry calculations for molecular systems, including geometry optimization, frequency analysis, and energy calculations.

## Features

- **Batch Processing**: Process multiple `.gjf` files simultaneously
- **Geometry Optimization & Frequency Analysis**: Automatic optimization and frequency checks
- **BSSE Correction**: Counterpoise correction for basis set superposition error
- **Multiple Calculation Methods**: Support for various DFT/functionals and basis sets
- **Energy Calculations**: Extract and compare energies across different methods
- **Data Export**: Save results to CSV files for analysis

## Requirements

- Python 3.x
- Gaussian 16 software installed
- Windows environment (currently configured for Windows)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/Gauss.git
   ```

2. Install dependencies (if any additional packages are needed):
   ```bash
   pip install -r requirements.txt
   ```
   
   *(Currently the script only uses standard library modules)*

3. Update the `GAUSSIAN_DIR` variable in the script to point to your Gaussian installation directory:
   ```python
   GAUSSIAN_DIR = r"C:\path\to\your\Gaussian\installation"
   ```

## Configuration

The script includes several configuration options:

- `OPTIMIZATION_METHOD`: Default method for geometry optimization and frequency calculation
- `AVAILABLE_METHODS`: List of calculation methods to choose from during execution
- `GAUSSIAN_DIR`: Path to your Gaussian installation directory
- `ENERGY_CONVERSION_FACTOR`: Conversion factor from Hartree to kJ/mol

## Usage

Run the script directly:

```bash
python bsse_gaussian_runner.py
```

The script will guide you through:

1. Setting up the Gaussian environment
2. Selecting `.gjf` files to process
3. Choosing calculation methods
4. Deciding whether to apply BSSE correction
5. Processing files and extracting energies

### Output Files

- `.out` files: Gaussian output files
- `_optimized.gjf` files: Optimized geometries
- CSV files: Collected energy data for analysis

## File Formats

The tool works with Gaussian `.gjf` input files. The script automatically detects the number of molecules (monomers, dimers, etc.) based on the filename pattern.

## BSSE Correction

The tool implements BSSE correction using the counterpoise method. For multimers (dimers, trimers, etc.), it:

1. Identifies fragments based on atomic distances
2. Applies the `counter=` parameter in the route section
3. Extracts the counterpoise-corrected energy from the output

## Troubleshooting

- Ensure Gaussian is properly installed and licensed
- Verify the `GAUSSIAN_DIR` path is correct
- Check that `.gjf` files have the correct format
- Monitor calculation timeouts and adjust if necessary

## Contributing

Feel free to submit issues and enhancement requests. Pull requests are welcome for bug fixes and improvements.

## License

MIT License - see the [LICENSE](./LICENSE) file for details.