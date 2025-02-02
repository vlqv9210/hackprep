# LinkUp

Inspiration Finding the right mentor can be a game-changer, but many aspiring professionals struggle to connect with experienced mentors in their field. Platforms like LinkedIn provide access to professionals, but reaching out can feel intimidating, and finding someone willing to guide you is challenging. We wanted to create a solution that simplifies mentorship matching by providing users with personalized mentor recommendations based on their interests, goals, and career paths.

What it does LinkUp is a mentorship matching platform that helps users find and connect with experienced professionals based on their career interests and aspirations. Users input a LinkedIn profile link, and our system analyzes relevant data to generate a list of potential mentors. The platform provides details such as the mentor’s job title, education, experience, and a pre-generated cold message template to help users initiate meaningful conversations.

![linkupgif](https://github.com/user-attachments/assets/5912d126-171d-4664-9612-7da5daa56cda)


## Tech Stack
- **Frontend**: React, Tailwind CSS
- **Backend**: Python, Proxycurl API, OpenRouter API, Flask
- **Database**: SQLAlchemy, SQLite

## Contributors
1. Van Phat Pham
2. Eusang Yu
3. Vy Vuong

## Features
- **Seamless Matching**: Smart algorithms pair mentors and mentees based on skills, goals, and interests.
- **Modern UI/UX**: Built with React and styled using Tailwind CSS for a sleek, responsive design.
- **User Profiles**: Easily browse and connect with mentors and mentees.
- **Messaging System**: Communicate directly within the platform.
- **Search & Filtering**: Find the right match quickly with advanced search options.

## What's next for LinkUp Enhanced AI Matching: 
- Improve mentor recommendations by incorporating skills, industries, and career goals. 
- Profile Customization: Allow users to refine search criteria for more personalized mentor suggestions. 
- Automated Outreach: Enable users to send AI-crafted messages directly through the platform. 
- Mobile-Friendly Version: Optimize the UI for better mobile accessibility. 
- Integration with More Platforms: Expand beyond LinkedIn to include other professional networks.



## Getting Started
### Prerequisites
Ensure you have the following installed:
- Node.js (v16 or higher)
- npm or yarn
- Python (v3.8 or higher)

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/linkup.git
   cd linkup
   ```
2. Install frontend dependencies:
   ```sh
   npm install
   # or
   yarn install
   ```
3. Install backend dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Start the development server:
   ```sh
   npm run dev
   # or
   yarn dev
   ```
5. Open `http://localhost:3000` in your browser.

## Folder Structure
```
linkup/
├── public/          # Static assets
├── src/             # Main application source code
│   ├── components/  # Reusable UI components
│   ├── pages/       # Application pages
│   ├── styles/      # Global and component styles
│   ├── utils/       # Helper functions
│   ├── hooks/       # Custom React hooks
│   ├── context/     # Context providers for global state
├── backend/         # Python backend
│   ├── api/         # API integration with Proxycurl and Llama
│   ├── models/      # Data models
│   ├── main.py      # Entry point for backend
├── .gitignore       # Files to be ignored by Git
├── package.json     # Project dependencies and scripts
├── requirements.txt # Python dependencies
└── README.md        # Project documentation


## License
This project is licensed under the MIT License.

## Contact
For questions or feedback, feel free to reach out!

