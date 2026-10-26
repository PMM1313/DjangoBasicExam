# Workshop Inventory & Repair Management App

A Django web application for managing workshop equipment, inventory stock, suppliers, and equipment repairs. The application helps keep equipment organized, track stock changes, identify low-stock items, and record maintenance costs.

## Features

- **Dashboard:** View equipment statistics, stock quantities, low-stock items, open repairs, and maintenance costs.
- **Equipment management:** Create, view, update, and delete equipment records.
- **Category management:** Organize equipment into categories.
- **Stock management:** Record incoming and outgoing stock movements and automatically update stock quantities.
- **Stock validation:** Prevent stock quantities from becoming negative through stock movements.
- **Supplier management:** Maintain supplier contact information and associate suppliers with equipment.
- **Repair management:** Record equipment problems, repair progress, completion dates, and repair costs.
- **Low-stock monitoring:** Identify equipment whose available quantity falls below its minimum stock threshold.
- **Form validation:** Validate user input and display validation errors.
- **Responsive navigation:** Navigate between the main application sections.

## Technologies

- Python
- Django
- SQLite
- HTML
- CSS

## Requirements

- Python 3.14
- pip

## Installation and Setup

### 1. Clone the repository


git clone https://github.com/PMM1313/DjangoBasicExam.git
cd DjangoBasicExam


### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Apply database migrations

The project uses SQLite for local development.

```bash
python manage.py migrate
```

No pre-populated database records are required. 
Create the initial categories, suppliers, and equipment through the application's interface.

### 5. Start the development server

```bash
python manage.py runserver
```

Open the local development address in your browser:

http://127.0.0.1:8000/

## Using the Application

1. Open the dashboard to review the current workshop overview.
2. Create equipment categories.
3. Add suppliers.
4. Create equipment records and associate them with categories and suppliers.
5. Use stock movements to record received or removed stock.
6. Record equipment repairs and update their status as work progresses.
7. Review low-stock equipment and maintenance costs on the dashboard.

Stock quantities are managed through stock movements rather than edited directly in the equipment form.

## Database

The application uses SQLite for local development. Django migrations create the database schema.

To initialize a fresh database, run:

```bash
python manage.py migrate
```

The application can then be populated through its user interface.

## Environment Variables and Credentials

Not needed.

## Development Notes

- Run `python manage.py makemigrations` after making model changes.
- Run `python manage.py migrate` to apply new migrations.

## License

This project was developed as a Django Basics course examination project.
