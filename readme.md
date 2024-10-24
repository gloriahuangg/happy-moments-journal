# Happy Moments Journal

Happy Moments Journal is a Streamlit-based web application that allows users to record and revisit their happy moments. It's designed to boost mood and promote positive thinking by encouraging users to document their joyful experiences and randomly recall them later.

## Features

- User registration and login system
- Add happy moments with text descriptions and optional images
- View random happy moments from the past
- Simple and intuitive user interface

## Installation

1. Clone this repository:
2. git clone https://github.com/gloriahuangg/happy-moments-journal.git cd happy-moments-journal


2. Create a virtual environment (optional but recommended):
python -m venv venv source venv/bin/activate # On Windows, use venv\Scripts\activate


3. Install the required packages:
pip install streamlit bcrypt pillow


## Usage

1. Run the Streamlit app:
streamlit run app.py


2. Open your web browser and go to `http://localhost:8501` (or the URL provided in the terminal).

3. Sign up for a new account or log in if you already have one.

4. Use the "Add Happy Moment" tab to record new happy moments.

5. Use the "View Random Happy Moment" tab to revisit a random happy memory when you need a mood boost.

## File Structure

- `app.py`: The main Streamlit application file containing all the code.
- `happy_journal.db`: SQLite database file (will be created automatically when the app runs).

## Dependencies

- Streamlit
- bcrypt
- Pillow (PIL)
- SQLite (included in Python standard library)

## Security Notes

- Passwords are hashed using bcrypt before storing in the database.
- The application uses Streamlit's built-in session state for user authentication.
- For production use, consider implementing additional security measures and using environment variables for sensitive information.

## Future Improvements

- Implement email verification for user registration
- Add ability to edit or delete moments
- Implement a calendar view to see happy moments by date
- Add data export functionality
- Improve error handling and input validation
