# Fitness Tracker Project

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
The **Fitness Tracker** is a web-based application designed to help users monitor and improve their health and fitness. The platform offers a BMI calculator, personalized exercise recommendations, and tools to track daily activities, providing a comprehensive solution for achieving a healthier lifestyle.

## Features
- **BMI Calculator:** Calculate your Body Mass Index (BMI) by entering your age, gender, height, and weight.
- **Exercise Recommendations:** Get personalized exercise tips based on your weight status (underweight, normal, or overweight).
- **Activity Tracker:** Log and track your workouts, including duration, type of exercise, and calories burned.
- **Progress Monitoring:** View progress over time to stay motivated and on track with your goals.
- **User-Friendly Interface:** Stylish and intuitive design for an enjoyable user experience.

## Technologies Used
- **Frontend:**
  - HTML5, CSS3, JavaScript
  - Responsive design using CSS Flexbox/Grid
- **Backend:**
  - Flask (Python)
  - MySQL for database management
- **APIs and Libraries:**
  - Flask-SQLAlchemy
  - Jinja2 templating engine

## Setup Instructions
Follow these steps to set up the project on your local machine:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/fitness-tracker.git
   cd fitness-tracker
   ```

2. **Set Up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database:**
   - Create a MySQL database (e.g., `fitness_db`).
   - Update the database configuration in the `config.py` file.
   - Run the following command to initialize the database:
     ```bash
     flask db init
     flask db migrate
     flask db upgrade
     ```


5. **Run the Application:**
   ```bash
   flask run
   ```
   Access the app at `http://127.0.0.1:5000/` in your browser.

## Usage
1. **Home Page:** View the dashboard with an overview of your fitness goals and progress.
2. ![image](https://github.com/user-attachments/assets/90155519-3fed-40ee-9b47-30297fedd98d)

3. **BMI Calculator:** Navigate to the BMI calculator page, enter your details, and get your BMI result.
4. ![image](https://github.com/user-attachments/assets/2e50c6e1-8ae5-469b-a88a-702b5459debc)

5. **Exercise Recommendations:** Receive tailored exercise suggestions based on your BMI.
6. ![image](https://github.com/user-attachments/assets/d609c944-18cd-4b01-b22e-0e44cf1f4ed2)

7. **Track Workouts:** Log your daily activities, view past records, and monitor progress.
8. ![image](https://github.com/user-attachments/assets/7c6c01d0-5f44-49d7-a1cc-a81fd5767c8f)


## Contributing
Contributions are welcome! Follow these steps to contribute:
1. Fork the repository.
2. Create a new branch for your feature/bug fix.
3. Commit your changes and push the branch.
4. Open a pull request for review.

## License
This project is licensed under the [MIT License](LICENSE).

---

Feel free to suggest improvements or report issues in the repository. Let’s build a healthier future together!

