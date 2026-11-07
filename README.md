# 💰 Spendly — Personal Expense Tracker

Spendly is a streamlined personal finance management application designed to help users track their daily spending, categorize expenses, and gain insights into their financial habits through a clean, professional dashboard.

## 🚀 Key Features

- **User Authentication**: Secure registration and login system with password hashing using `Werkzeug`.
- **Expense CRUD**: Full Create, Read, Update, and Delete functionality for managing personal transactions.
- **Dynamic Dashboard**: A profile page featuring summary statistics (Total Spent, Transaction Count, Top Category).
- **Advanced Filtering**: Date-range filters with presets (This Month, Last 3 Months, Last 6 Months) to analyze spending over specific periods.
- **Category Analytics**: A visual breakdown of spending by category with percentage calculations.
- **Responsive Design**: A modern, clean UI built with Flask templates and custom CSS.

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite (using raw SQL for performance and clarity)
- **Frontend**: HTML5, CSS3, Jinja2 Templates
- **Security**: Password hashing with `Werkzeug`, session-based authentication, and parameterized SQL queries to prevent injection.

## 🎓 The "Claude Code" Learning Experience

The most significant aspect of this project was not just the code itself, but the workflow used to build it. This project was developed using **Claude Code**, Anthropic's official CLI for Claude.

### What I Mastered with Claude Code:
Building this application allowed me to move beyond simple chat-based AI and embrace an **Agentic Development Workflow**. I learned how to:
- **Iterative Spec-Driven Development**: Using the `/create-spec` workflow to define features before implementation, ensuring architectural consistency.
- **Plan Mode Execution**: Leveraging `/plan` to architect complex changes and verify them before touching the codebase.
- **Autonomous Research**: Utilizing Claude Code's ability to explore the file system, read multiple files, and identify patterns independently.
- **CLI-Integrated Debugging**: Running the application, analyzing traceback errors in the terminal, and applying fixes in real-time.
- **Git Integration**: Managing feature branches and merging changes directly through the AI agent.

This experience demonstrated a paradigm shift in software engineering: moving from "writing code" to "orchestrating AI agents" to build robust, production-ready software.

## 🏁 Getting Started

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Installation & Setup
1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd expense-tracker-claude-code
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python3 app.py
   ```
   The app will be available at `http://127.0.0.1:5001`

## 📄 License
This project is for educational purposes as part of a learning journey with Claude Code.
