import { useState } from "react";
import axios from "axios";
import { FaBriefcase, FaGraduationCap, FaStar, FaCommentAlt } from "react-icons/fa";
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/swiper-bundle.css";

const MentorCard = ({ mentor }) => (
    <div className="bg-white p-6 rounded-lg shadow-lg max-w-xl w-full mx-auto">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">{mentor.name}</h2>
<<<<<<< HEAD
        <p className="text-lg font-semibold text-indigo-600">
            {mentor.job_title}
        </p>
        <p className="text-gray-700 mt-2">{mentor.skills}</p>
        <p className="text-gray-700 mt-2">
            <strong>Education:</strong> {mentor.education}
        </p>
        <p className="text-gray-700 mt-2">
            <strong>Experience:</strong> {mentor.experience} years
        </p>
        <p className="text-gray-700 mt-2">
            <strong>Explanation:</strong> {mentor.explanation}
        </p>
        <p className="text-gray-700 mt-2">
            <strong>Message:</strong> {mentor.cold_message}
=======
        <p className="text-lg font-semibold text-indigo-600 flex items-center mb-2">
            <FaBriefcase className="mr-2" />
            {mentor.job_title}
        </p>
        <p className="text-gray-700 mt-2 mb-2 flex items-center">
            <FaGraduationCap className="mr-2" />
            {mentor.education}
        </p>
        <p className="text-gray-700 mt-2 mb-2 flex items-center">
            <FaStar className="mr-2" />
            {mentor.score}
        </p>
        <p className="text-gray-700 mt-2 mb-2 flex items-center">
            <FaCommentAlt className="mr-2" />
            {mentor.cold_message}
>>>>>>> 378e210 (fix the display of cards)
        </p>
    </div>
);

const Loader = () => (
    <div className="text-xl font-semibold text-gray-700">Loading mentors...</div>
);

const api = axios.create({
    baseURL: "http://127.0.0.1:5000/",
});

function App() {
    const [url, setUrl] = useState("");
    const [mentors, setMentors] = useState([]);
    const [loading, setLoading] = useState(false);
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
                });

                // Now fetch mentors after URL submission
                fetchMentors();
            }
        } catch (e) {
            setMessage({
                type: "error",
                text: "Failed to submit URL. Try again." + e,
            });
            setLoading(false);
        }
    };

    const fetchMentors = async () => {
        try {
            setLoading(true); // Start loading
            const response = await api.post("/testAIApi", {});

            if (response.status === 200) {
                setMessage({
                    type: "success",
                    text: "Mentors fetched successfully!",
                });

                // Delay message timeout
                setTimeout(() => {
                    setMessage(null);
                }, 3000);
            }

            const mentorData = response["data"]["message"];
            setMentors(mentorData);
            setLoading(false);
        } catch (e) {
            setMessage({
                type: "error",
                text: "Failed to fetch mentors. Try again." + e,
            });
            setLoading(false);
        }
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
                            message.type === "success" ? "bg-green-500" : "bg-red-500"
                        }`}
                    >
                        {message.text}
                    </div>
                )}

                {/* Loading or Mentor Cards */}
                {loading ? (
                    <Loader />
                ) : (
                    mentors.length > 0 && (
                        <Swiper
                            slidesPerView={4} // 4 cards per slide
                            spaceBetween={20}
                            loop={true}
                            autoplay={{
                                delay: 3000,
                                disableOnInteraction: false,
                            }}
                            breakpoints={{
                                640: {
                                    slidesPerView: 2, // 2 cards per slide on small screens
                                },
                                768: {
                                    slidesPerView: 3, // 3 cards per slide on medium screens
                                },
                                1024: {
                                    slidesPerView: 4, // 4 cards per slide on larger screens
                                },
                            }}
                        >
                            {/* Generate 10 mentor cards */}
                            {mentors.map((mentor, index) => (
<<<<<<< HEAD
                                <MentorCard key={index} mentor={mentor} />
=======
                                <SwiperSlide key={index}>
                                    <MentorCard mentor={mentor} />
                                </SwiperSlide>
>>>>>>> 378e210 (fix the display of cards)
                            ))}
                        </Swiper>
                    )
                )}
            </div>
        </div>
    );
}

export default App;
