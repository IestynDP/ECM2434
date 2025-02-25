Sustainability Gamification App

📌 Overview

The Sustainability Gamification App is a Django-based web application designed to encourage users to adopt environmentally friendly habits through gamification. Users can earn points for sustainable actions, take quizzes to test their environmental knowledge, and compete on leaderboards. The project aims to educate users on sustainability while making the process engaging and rewarding.

⚙️ Installation Guide

Prerequisites

Python 3.12.4

pip (Python package manager)

SQLite3 (bundled with Python but ensure it is installed)

Setup Instructions

Clone the repository:
git clone https://github.com/IestynDP/ECM2434.git
cd IestynDP/ECM2434

Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Apply database migrations:
python manage.py migrate

Run the development server:
python manage.py runserver

Open the app in your browser:
http://127.0.0.1:8000/

🏆 Core Features

User Authentication: Users can register, log in, and edit their profiles.

Gamification System:

Earn points for sustainable activities (e.g., visiting sustainable restaurants, answering quiz questions).

Compete on a Leaderboard based on points earned.

Sustainability Quiz:

Users answer environment-related questions to earn points.

Check-In System (QR Placeholder):

Users can check into verified locations to gain sustainability points (currently using a placeholder system).

Business Listings:

Admins can add sustainable restaurants to the system, to which users can check in and gain points for visiting.

🛠 Development & Contribution

If you'd like to contribute, please follow the setup guide above. For significant changes, create a new branch and submit a pull request.

🧪 Running Tests

Test cases are included to ensure core functionality is working correctly.
To run tests:

python manage.py test

⚠️ Known Issues & Future Plans

Current Issues:

UI/UX needs major improvements for aesthetics and usability.

Limited ways to earn points beyond quizzes and check-ins.

Planned Features:

Expanded Point System: More activities to earn points.

Point Usage System: Implement a cosmetic shop where users can spend points.

Better Verification for Check-Ins: Implement a robust QR code validation system.

Enhanced Gamification: Add badges, achievements, and interactive sustainability challenges.

Improved Business Listings: Allow verified sustainable businesses to sign up.

📜 License

This project is licensed under the MIT License.