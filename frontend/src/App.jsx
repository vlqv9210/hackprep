import { useState, useRef } from "react";
import axios from "axios";
import {
    FaBriefcase,
    FaGraduationCap,
    FaStar,
    FaCommentAlt,
} from "react-icons/fa";
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/swiper-bundle.css";
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";

const MentorCard = ({ mentor }) => (
    <div className="bg-white p-6 rounded-lg shadow-xl max-w-xl w-full mx-auto transform hover:scale-105 transition-transform duration-300 ease-in-out">
        <h2 className="text-2xl font-bold text-gray-800 mb-2">{mentor.name}</h2>
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
        </p>
    </div>
);

function Home({
    url,
    setUrl,
    handleSubmit,
    message,
    loading,
    mentors,
    swiperRef,
}) {
    return (
        <div className="flex-1 p-6 md:p-12 text-center">
            <h1 className="text-3xl font-bold mb-6 text-indigo-600">
                Find Your Mentor
            </h1>
            <div className="mb-4 flex flex-col items-center">
                <input
                    type="url"
                    placeholder="Enter URL"
                    className="w-full sm:w-96 md:w-1/2 lg:w-1/3 p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
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
            {loading ? (
                <Loader />
            ) : (
                mentors.length > 0 && (
                    <Swiper
                        ref={swiperRef}
                        slidesPerView={4}
                        spaceBetween={20}
                        loop={true}
                        autoplay={{ delay: 3000, disableOnInteraction: false }}
                    >
                        {mentors.map((mentor, index) => (
                            <SwiperSlide key={index}>
                                <MentorCard mentor={mentor} />
                            </SwiperSlide>
                        ))}
                    </Swiper>
                )
            )}
        </div>
    );
}

const Loader = () => (
    <div className="text-xl font-semibold text-gray-700">
        Loading mentors...
    </div>
);

const api = axios.create({
    baseURL: "http://127.0.0.1:5000/",
});

function App() {
    const swiperRef = useRef(null);
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
            setLoading(true);
            // "/linkedinProfile" 2 times left
            // after that if want to try run
            // change to "/testAIApi"
            // and uncomment the fetchMentors()
            const response = await api.post("/linkedinProfile", {
                linkedin_url: url,
            });
            if (response.status === 200) {
                setMessage({
                    type: "success",
                    text: "URL submitted successfully!",
                });
                setTimeout(() => setMessage(null), 500);
            }
            const mentorData = response["data"]["message"];
            setMentors(mentorData);
            setLoading(false);

            // fetchMentors()
        } catch (e) {
            setMessage({
                type: "error",
                text: "Failed to submit URL. Try again." + e,
            });
            setLoading(false);
        }
    };

    // const fetchMentors = async () => {
    //     try {
    //         setLoading(true);
    //         const response = await api.post("/testAIApi", {});
    //         if (response.status === 200) {
    //             setMessage({
    //                 type: "success",
    //                 text: "Mentors fetched successfully!",
    //             });
    //             setTimeout(() => setMessage(null), 500);
    //         }
    //         const mentorData = response["data"]["message"];
    //         setMentors(mentorData);
    //         setLoading(false);
    //     } catch (e) {
    //         setMessage({
    //             type: "error",
    //             text: "Failed to fetch mentors. Try again." + e,
    //         });
    //         setLoading(false);
    //     }
    // };

    return (
        <Router>
            <div className="min-h-screen bg-gray-50 flex flex-col">
                <nav className="bg-indigo-600 text-white py-4 px-6 flex justify-between items-center shadow-md">
                    <div className="flex items-center">
                        <Link to="/" className="text-lg font-bold">
                            LinkUp
                        </Link>
                    </div>
                    <div>
                        <Link to="/about" className="text-white mx-4">
                            About
                        </Link>
                        <Link to="/mission" className="text-white">
                            Mission
                        </Link>
                    </div>
                </nav>

                <Routes>
                    <Route
                        path="/about"
                        element={
                            <div className="p-6 md:p-12 text-center">
                                <h1 className="text-3xl font-bold mb-6 text-indigo-600">
                                    About Us
                                </h1>
                                <p className="text-lg text-gray-700">
                                    We are SU <h4></h4>ackathon team
                                </p>
                            </div>
                        }
                    />

                    <Route
                        path="/mission"
                        element={
                            <div className="p-6 md:p-12 text-center">
                                <h1 className="text-3xl font-bold mb-6 text-indigo-600">
                                    Our Mission
                                </h1>
                                <p className="text-lg text-gray-700">
                                    We want to help young generation to find
                                    their mentor for their brighter future
                                </p>
                            </div>
                        }
                    />

                    <Route
                        path="/"
                        element={
                            <Home
                                url={url}
                                setUrl={setUrl}
                                handleSubmit={handleSubmit}
                                message={message}
                                loading={loading}
                                mentors={mentors}
                                swiperRef={swiperRef}
                            />
                        }
                    />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
