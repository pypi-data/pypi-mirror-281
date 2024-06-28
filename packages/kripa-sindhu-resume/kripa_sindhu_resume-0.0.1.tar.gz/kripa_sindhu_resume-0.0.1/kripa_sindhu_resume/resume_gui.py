import sys
import time

class Resume:
    def __init__(self):
        self.data = {
            "name": "Kripa Sindhu",
            "contact": {
                "email": "kripa.sindhu21b@iiitg.ac.in",
                "phone": "+91-9693077256",
                "github": "https://github.com/kripa-sindhu-007",
                "website": "https://kripa-sindhu007.netlify.app/",
                "linkedin": "https://www.linkedin.com/in/kripa-sindhu-9090041b9/"
            },
            "education": [
                {
                    "institution": "Indian Institute of Information Technology, Guwahati",
                    "degree": "B.Tech Computer Science and Engineering",
                    "dates": "December 2021 – April 2025"
                },
                {
                    "institution": "S.K.P Vidya Vihar, Bhagalpur",
                    "degree": "High School",
                    "dates": "February 2020"
                }
            ],
            "coursework": [
                "Object-Oriented Programming",
                "Data Structures & Algorithms",
                "Computer Networks",
                "Database Management System",
                "Operating System",
                "Machine Learning",
                "Cloud Computing",
                "Discrete Math"
            ],
            "skills": {
                "languages": ["C/C++", "Python", "JavaScript", "HTML/CSS"],
                "tools": ["Git/GitHub", "VS Code", "Google Collab"],
                "frameworks": ["ReactJS", "NodeJs"],
                "libraries": ["pandas", "NumPy", "Matplotlib"],
                "soft_skills": ["Process Oriented", "Teamwork"]
            },
            "projects": [
                {
                    "name": "Digit Recognition using Machine Learning",
                    "technologies": ["TensorFlow", "Keras", "OpenCV", "NumPy"],
                    "date": "June 2023",
                    "description": [
                        "Implemented TensorFlow and Keras to train a convolutional neural network achieving 99.21% accuracy in digit recognition",
                        "Leveraged OpenCV for image preprocessing, reducing processing time.",
                        "Optimized numerical operations using NumPy, resulting in a faster computation speed"
                    ]
                },
                {
                    "name": "Personal Website",
                    "technologies": ["Frontend Development", "ReactJS"],
                    "date": "May 2023",
                    "description": [
                        "Developed a responsive personal portfolio website, increasing user engagement.",
                        "Implemented smooth transitions and navigation."
                    ]
                },
                {
                    "name": "Math-Quiz",
                    "technologies": ["Python Development", "Kivy MD"],
                    "date": "December 2022",
                    "description": [
                        "Developed a simple Math Quiz game using the Python programming language",
                        "Utilized KivyMD for intuitive interface design."
                    ]
                },
                {
                    "name": "Tic-Tac-Toe",
                    "technologies": ["Python Development", "Tkinter GUI"],
                    "date": "December 2022",
                    "description": [
                        "Developed a popular Tic-Tac-Toe game with Python",
                        "Utilized Tkinter for smooth graphical interface, receiving positive feedback on user experience"
                    ]
                }
            ],
            "experience": [
                {
                    "role": "Member",
                    "organization": "Competitive Programming Club",
                    "dates": "January 2022 – Present",
                    "description": "Involved in the club centered around Competitive Programming"
                }
            ],
            "achievements": [
                "Qualified GATE-2024 CSE among the top 5% of total appeared candidates.",
                "3 star on CodeChef and solved 500+ DSA questions across platforms"
            ]
        }

    def get_resume_data(self):
        return self.data

def print_slow(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

def display_resume_cli():
    resume = Resume()
    resume_data = resume.get_resume_data()

    print("\n")
    print_slow("\033[1;32m" + resume_data['name'].center(50) + "\n")
    print("\033[0m")

    print_slow("\n\033[1;36mContact Information\033[0m\n")
    for key, value in resume_data['contact'].items():
        print_slow(f"  \033[1;34m- {key.capitalize()}:\033[0m {value}\n")
    print("\n")

    print_slow("\033[1;36mEducation\033[0m\n")
    for edu in resume_data['education']:
        print_slow(f"  \033[1;34m- {edu['degree']} in {edu['institution']} ({edu['dates']})\033[0m\n")
    print("\n")

    print_slow("\033[1;36mCoursework\033[0m\n")
    for course in resume_data['coursework']:
        print_slow(f"  \033[1;34m- {course}\033[0m\n")
    print("\n")

    print_slow("\033[1;36mSkills\033[0m\n")
    for skill_type, skill_list in resume_data['skills'].items():
        print_slow(f"  \033[1;34m * {skill_type.capitalize()}:\033[0m\n")
        for skill in skill_list:
            print_slow(f"    \033[1;34m- {skill}\033[0m\n")
    print("\n")

    print_slow("\033[1;36mProjects\033[0m\n")
    for project in resume_data['projects']:
        print_slow(f"  \033[1;34m * {project['name']} ({project['date']})\033[0m\n")
        for desc in project['description']:
            print_slow(f"    \033[1;34m- {desc}\033[0m\n")
    print("\n")

    print_slow("\033[1;36mExperience\033[0m\n")
    for exp in resume_data['experience']:
        print_slow(f"  \033[1;34m * {exp['role']}, {exp['organization']} ({exp['dates']})\033[0m\n")
        print_slow(f"    \033[1;34m- {exp['description']}\033[0m\n")
    print("\n")

    print_slow("\033[1;36mAchievements\033[0m\n")
    for achievement in resume_data['achievements']:
        print_slow(f"  \033[1;34m- {achievement}\033[0m\n")

if __name__ == "__main__":
    display_resume_cli()
