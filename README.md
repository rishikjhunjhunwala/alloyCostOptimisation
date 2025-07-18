# Alloy Optimizer

Django-based web application for optimizing alloy formulations using linear programming to determine the most cost-effective mix of scrap materials that meet specific composition requirements.

## Features

### Core Functionality
- **Linear Programming Optimization**: Uses PuLP library for cost minimization
- **Multi-Product Batch Processing**: Optimize multiple products simultaneously
- **CSV Data Management**: Upload and manage scrap data and composition requirements
- **Results Export**: Download optimization results in CSV format
- **Responsive Web Interface**: Bootstrap-based UI with mobile support

### Phase 1.1 - Organization-based Access Control ✅
- **Multi-tenant Architecture**: Complete organization-based data isolation
- **User Management**: Extended user profiles with organization assignment
- **Enhanced Security**: Cross-organization access prevention
- **Organization Context**: UI displays current organization throughout interface
- **Admin Interface**: Organization-scoped administration

## Technology Stack

- **Backend**: Django 4.2.7, Python 3.11+
- **Optimization**: PuLP (Linear Programming)
- **Database**: SQLite (development), PostgreSQL-ready
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Data Processing**: Pandas, NumPy
- **Deployment**: Gunicorn, WhiteNoise

## Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git

### Setup
```bash
# Clone repository
git clone <your-repository-url>
cd alloy-optimizer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Set up organizations (see Organization Setup below)

# Start development server
python manage.py runserver
```

### Organization Setup
After installation, create organizations and assign users:

```python
# Run: python manage.py shell
from django.contrib.auth.models import User
from optimizer.models import Organization, UserProfile

# Create organizations
admin_org = Organization.objects.create(
    name="Admin Organization",
    code="ADMIN",
    description="Administrative organization"
)

demo_org = Organization.objects.create(
    name="Demo Company", 
    code="DEMO",
    description="Demo organization"
)

# Assign superuser to admin organization
superuser = User.objects.filter(is_superuser=True).first()
UserProfile.objects.create(
    user=superuser,
    organization=admin_org,
    employee_id="ADMIN001",
    department="Administration"
)
```

## Usage

### Data Upload
1. **Scrap Data**: Upload CSV with scrap material compositions and costs
2. **Composition Requirements**: Upload CSV with product specifications

### Batch Optimization
1. Create optimization batch
2. Add products with required amounts
3. Run optimization to get cost-effective material mix
4. Download results

### File Formats

#### Scrap Data CSV
```csv
Scrap_Type,COST,SI,FE,CU,MN,MG,Available_Amount
Primary Aluminium,207.75,0.04,0.06,0,0,0,100
```

#### Composition Requirements CSV
```csv
Product,Amount,SI_MIN,SI_MAX,FE_MIN,FE_MAX,CU_MIN,CU_MAX,MN_MIN,MN_MAX,MG_MIN,MG_MAX
AC2BF,10,0.055,0.065,0.003,0.004,0.031,0.038,0.0001,0.0001,0.003,0.005
```

## Project Structure

```
alloy_optimizer/
├── alloy_optimizer/          # Django project settings
├── optimizer/                # Main application
│   ├── models.py            # Database models
│   ├── views.py             # Application views
│   ├── forms.py             # Form definitions
│   ├── admin.py             # Admin interface
│   ├── middleware.py        # Organization middleware
│   ├── migrations/          # Database migrations
│   └── templates/           # HTML templates
├── optimization/            # Linear programming solver
│   └── solver.py           # AlloyOptimizer class
├── requirements.txt         # Python dependencies
└── manage.py               # Django management script
```

## Development

### Phase Implementation Progress
- ✅ **Phase 1.1**: Organization-based Access Control (Complete)
- 🔄 **Phase 1.2**: Dynamic Element Support (Next)
- ⏳ **Phase 1.3**: Decimal Precision Standardization
- ⏳ **Phase 2**: User Experience Improvements
- ⏳ **Phase 3**: Enterprise Features & API

### Contributing
1. Fork the repository
2. Create feature branch: `git checkout -b feature/phase-x.x`
3. Make changes and test thoroughly
4. Commit with descriptive messages
5. Push and create pull request

### Database Migrations
```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

## Architecture

### Multi-tenant Design
- Organization-based data isolation
- User profiles with organization assignment
- Middleware-enforced access control
- Admin interface with organization boundaries

### Optimization Engine
- Linear programming using PuLP library
- Cost minimization objective
- Composition constraint satisfaction
- Support for multiple products in single batch

## Security

- Organization-based data isolation
- Cross-organization access prevention
- User authentication and authorization
- Admin interface security
- CSRF protection
- SQL injection protection via Django ORM

## License

Licensed under the Apache License, Version 2.0

## Support

- Check existing issues in repository
- Create new issue for bug reports or feature requests
- Follow development progress in PROJECT_ACTIVITY_LOG.md

---

**Current Version**: v1.1 (Organization Access Control)
**Last Updated**: [Current Date]
**Status**: Production Ready (Phase 1.1 Complete)