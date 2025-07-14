# Alloy Optimizer

A Django web application for optimizing aluminum alloy composition using linear programming.

## Description

Alloy Optimizer helps metal recycling and manufacturing companies determine the most cost-effective mix of scrap materials to meet specific alloy composition requirements. Using linear programming techniques, the application calculates optimal formulations while respecting constraints on element percentages (Silicon, Iron, Copper, Manganese, Magnesium).

## Features

- Upload and manage scrap material data (compositions, costs, availability)
- Upload and manage product composition requirements
- Create optimization batches with multiple products
- Run optimization to find the most economical material mix
- View and download optimization results

## Installation

1. Clone the repository
2. Install dependencies with `pip install -r requirements.txt`
3. Run migrations with `python manage.py migrate`
4. Create a superuser with `python manage.py createsuperuser`
5. Run the development server with `python manage.py runserver`

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE] file for details.

## Copyright

Copyright 2025 RISHIK JHUNJHUNWALA

## Notice

This project contains third-party software. See the [NOTICE] file for details.

## Keywords
Linear Programming, Blending Problem, Mixed Blending Problem, Alloys and Metals, Alumunium recycling, secondary aluminium, cost optimisation, optimization, scrap