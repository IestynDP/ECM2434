# Sustainability Gamification App
## 📌 Overview

The Sustainability Gamification App is a Django-based web application designed to encourage users to adopt environmentally friendly habits through gamification. Users can earn points for sustainable actions, take quizzes to test their environmental knowledge, and compete on leaderboards. The project aims to educate users on sustainability while making the process engaging and rewarding.
A big part of this is out food map! this shows sustainable resturants in Exeter.

## 📑 Table of Contents

- [Overview](#-overview)
- [Installation Guide](#-installation-guide)
- [Core Features](#-core-features)
- [Running Tests](#-running-tests)
- [Known Issues & Future Plans](#-known-issues--future-plans)
- [License](#-license)

## ⚙️ Installation Guide

### Prerequisites

- Python 3.12.4
- pip (Python package manager)
- SQLite3 (bundled with Python but ensure it is installed)

### Setup Instructions

1. Clone the repository:

   ```sh
   git clone https://github.com/IestynDP/ECM2434.git
   cd IestynDP/ECM2434
   ```

2. Create a virtual environment (optional but recommended):

   ```sh
   python -m venv venv
   source venv/bin/activate (macos/linux)
   venv\Scripts\activate (windows)
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Apply database migrations:

   ```sh
   python manage.py migrate
   ```

5. Run the development server:

   ```sh
   python manage.py runserver
   ```

6. Open the app in your browser:
   ```
   http://127.0.0.1:8000/
   ```

## 🏆 Core Features

- **User Authentication**: Users can register, log in, and edit their profiles.
- **Gamification System**:
  - Earn points for sustainable activities (e.g., visiting sustainable restaurants, answering quiz questions).
  - Compete on a Leaderboard based on points earned.
- **Sustainability Quiz**: Users answer environment-related questions to earn points.
- **Check-In System (QR Placeholder)**: Users can check into verified locations to gain sustainability points (currently using a placeholder system).
- **Business Listings**: Admins can add sustainable restaurants to the system, to which users can check in and gain points for visiting.

## 🧪 Running Tests

Test cases are included to ensure core functionality is working correctly. To run tests:

```sh
python manage.py test --verbosity=2
```

## ⚠️ Known Issues & Future Plans

### Current Issues:

- UI/UX needs major improvements for aesthetics and usability.
- Limited ways to earn points beyond quizzes and check-ins.

### Planned Features:

- Expanded Point System: More activities to earn points.
- Point Usage System: Implement a cosmetic shop where users can spend points.
- Better Verification for Check-Ins: Implement a robust QR code validation system.
- Enhanced Gamification: Add badges, achievements, and interactive sustainability challenges.
- Improved Business Listings: Allow verified sustainable businesses to sign up.

## 📜 [[LICENSE]](License)

This project is licensed under the MIT License.
