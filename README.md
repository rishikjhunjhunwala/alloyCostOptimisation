# Alloy Optimizer Project

## Overview

The Alloy Optimizer Project is a Python-based application designed to optimize the composition of scrap input for obtaining a output-mix with minimised cost. It leverages advanced algorithms to determine the best combination of materials to achieve desired chemical properties and cost-effectiveness.

The application achieves this with Linear Programming (PuLP) of Blended Problems.

## Features

- **Custom Alloy Optimization**: Define target properties and constraints to generate optimal alloy compositions.
- **Material Database Integration**: Utilize a built-in database of materials with their properties.
- **Cost Analysis**: Evaluate the cost implications of different alloy compositions.
- **User-Friendly Interface**: Simple and intuitive interface for defining requirements and viewing results.
- **Extensibility**: Easily extendable to include additional materials or optimization criteria.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd alloy_optimizer_project
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:

   ```bash
   python main.py
   ```

2. Follow the on-screen instructions to input your desired alloy properties and constraints.

3. View the optimized alloy composition and associated cost analysis.

## File Structure

- `main.py`: Entry point of the application.
- `optimizer/`: Contains the core optimization logic.
- `data/`: Includes material property datasets.
- `tests/`: Unit tests for the application.
- `requirements.txt`: List of Python dependencies.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or support, please contact [your-email@example.com].
