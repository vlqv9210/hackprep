import { useState } from "react";
import axios from "axios";

// MentorCard Component
const MentorCard = ({ name, expertise, image, rating }) => (
    <div className="bg-white p-6 border border-gray-300 rounded-lg shadow-lg flex flex-col items-center hover:shadow-xl transition-all duration-300 ease-in-out transform hover:scale-105 hover:bg-indigo-50">
        <img
            src={image}
            alt={name}
            className="w-24 h-24 rounded-full mb-4 object-cover"
        />
        <div className="text-lg font-semibold mb-2">{name}</div>
        <div className="text-sm text-gray-600">{expertise}</div>
        <div className="flex items-center mt-2">
            <span className="text-yellow-400">{"★".repeat(rating)}</span>
            <span className="text-gray-500 ml-2">{rating}/5</span>
        </div>
    </div>
);

// Loader Component
const Loader = () => (
    <div className="text-xl font-semibold text-gray-700">
        Loading mentors...
    </div>
);

const api = axios.create({
    baseURL: "http://127.0.0.1:5000/",
});

function App() {
    const [url, setUrl] = useState("");
    const [mentors, setMentors] = useState([]);
    const [loading, setLoading] = useState(false); // Default false since mentors shouldn't load initially
    const [message, setMessage] = useState(null);

    const handleSubmit = async () => {
        if (!url.trim()) {
            setMessage({ type: "error", text: "Please enter a valid URL." });
            return;
        }
        try {
            setLoading(true); // Start loading
            const response = await api.post("/testGetData", {
                linkedin_url: url,
            });

            if (response.status === 200) {
                setMessage({
                    type: "success",
                    text: "URL submitted successfully!",
                    message: response,
                });

                // Now fetch mentors after URL submission
                fetchMentors();
            }
        } catch (e) {
            setMessage({
                type: "error",
                text: "Failed to submit URL. Try again." + e,
            });
            setLoading(false); // Stop loading if error occurs
        }
    };

    const fetchMentors = async () => {
        try {
            setLoading(true); // Start loading
            const response = await api.post("/testAIApi", {});

            if (response.status === 200) {
                setMessage({
                    type: "success",
                    text: "URL submitted successfully!",
                });
            }

            const mentorData = response["data"]["message"];

            console.log(mentorData);
            setMentors(mentorData);
            setLoading(false);
        } catch (e) {
            setMessage({
                type: "error",
                text: "Failed to submit URL. Try again." + e,
            });
            setLoading(false); // Stop loading if error occurs
        }

        // đổi lại cho match với cái json này
        // {
        //   "name": "Jessica Brewer",
        //   "job_title": "DevOps Engineer",
        //   "skills": "Cloud Computing, C#, Software Design, C++, Docker",
        //   "education": "B.S. in Electrical Engineering",
        //   "experience": 34,
        //   "score": 45,
        //   "explanation": "Jessica's experience in DevOps and software design makes her a good match for Vy's skills, although their skill sets differ.",
        //   "cold_message": "Hi Jessica, I'm Vy, a data analysis student looking to learn more about DevOps. Can we discuss potential projects or collaborations?"
        // },

        // const mentorData = [
        //     {
        //         name: "Mentor 1",
        //         expertise: "Software Engineering",
        //         image: "https://randomuser.me/api/portraits/men/1.jpg",
        //         rating: 4,
        //     },
        //     {
        //         name: "Mentor 2",
        //         expertise: "Data Science",
        //         image: "https://randomuser.me/api/portraits/women/1.jpg",
        //         rating: 5,
        //     },
        //     {
        //         name: "Mentor 3",
        //         expertise: "AI/ML",
        //         image: "https://randomuser.me/api/portraits/men/2.jpg",
        //         rating: 3,
        //     },
        //     {
        //         name: "Mentor 4",
        //         expertise: "Web Development",
        //         image: "https://randomuser.me/api/portraits/men/3.jpg",
        //         rating: 4,
        //     },
        //     {
        //         name: "Mentor 5",
        //         expertise: "Cybersecurity",
        //         image: "https://randomuser.me/api/portraits/women/2.jpg",
        //         rating: 5,
        //     },
        // ];
        // setMentors(mentorData);
        // setLoading(false);
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col">
            <nav className="bg-indigo-600 text-white py-4 px-6 flex justify-between items-center shadow-md">
                <div className="text-lg font-bold">Mentorship Platform</div>
            </nav>

            <div className="flex-1 p-6 md:p-12 text-center">
                <h1 className="text-3xl font-bold mb-6">Find a Mentor</h1>

                {/* URL Input */}
                <div className="mb-4 flex flex-col items-center">
                    <input
                        type="url"
                        placeholder="Enter URL"
                        className="w-full sm:w-96 md:w-1/2 lg:w-1/3 p-3 border border-gray-300 rounded-md shadow-sm"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                    />
                    <button
                        onClick={handleSubmit}
                        className="mt-3 bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 transition"
                    >
                        Submit
                    </button>
                </div>

                {/* Message Feedback */}
                {message && (
                    <div
                        className={`mt-2 p-2 rounded-md text-white ${
                            message.type === "success"
                                ? "bg-green-500"
                                : "bg-red-500"
                        }`}
                    >
                        {message.text}
                    </div>
                )}

                {/* Loading or Cards */}
                {loading ? (
                    <Loader />
                ) : (
                    mentors.length > 0 && (
                        <div className="grid grid-cols-1 sm:grid-cols-2 md-grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6 w-full max-w-6xl mx-auto">
                            {mentors.map((mentor, index) => (
                                <MentorCard
                                    key={index}
                                    name={mentor.name}
                                    job_title={mentor.job_title}
                                    experience={mentor.experience}
                                    score={mentor.score}
                                />
                            ))}
                        </div>
                    )
                )}
            </div>
        </div>
    );
}

export default App;
