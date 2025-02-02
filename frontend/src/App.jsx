import { useState, useRef } from "react";
import axios from "axios";
import { FaBriefcase, FaGraduationCap, FaStar, FaCommentAlt } from "react-icons/fa";
import { Swiper, SwiperSlide } from "swiper/react";
import "swiper/swiper-bundle.css";
import { BrowserRouter as Router, Route, Link, Switch } from "react-router-dom";

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

const Loader = () => (
    <div className="text-xl font-semibold text-gray-700">Loading mentors...</div>
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
            const response = await api.post("/testGetData", { linkedin_url: url });
            if (response.status === 200) {
                setMessage({ type: "success", text: "URL submitted successfully!" });
                fetchMentors();
            }
        } catch (e) {
            setMessage({ type: "error", text: "Failed to submit URL. Try again." + e });
            setLoading(false);
        }
    };

    const fetchMentors = async () => {
        try {
            setLoading(true);
            const response = await api.post("/testAIApi", {});
            if (response.status === 200) {
                setMessage({ type: "success", text: "Mentors fetched successfully!" });
                setTimeout(() => setMessage(null), 500);
            }
            const mentorData = response["data"]["message"];
            setMentors(mentorData);
            setLoading(false);
        } catch (e) {
            setMessage({ type: "error", text: "Failed to fetch mentors. Try again." + e });
            setLoading(false);
        }
    };

    return (
        <Router>
            <div className="min-h-screen bg-gray-50 flex flex-col">
                <nav className="bg-indigo-600 text-white py-4 px-6 flex justify-between items-center shadow-md">
                    {/* Navigation Links */}
                    <div className="flex items-center">
                        <div className="text-lg font-bold">LinkUp</div>
                    </div>
                    <div>
                        <Link to="/about" className="text-white mx-4">About</Link>
                        <Link to="/mission" className="text-white">Mission</Link>
                    </div>
                </nav>

                <Switch>
                    <Route path="/about">
                        <div className="p-6 md:p-12 text-center">
                            <h1 className="text-3xl font-bold mb-6 text-indigo-600">About Us</h1>
                            <p className="text-lg text-gray-700">This is the About page content.</p>
                        </div>
                    </Route>

                    <Route path="/mission">
                        <div className="p-6 md:p-12 text-center">
                            <h1 className="text-3xl font-bold mb-6 text-indigo-600">Our Mission</h1>
                            <p className="text-lg text-gray-700">This is the Mission page content.</p>
                        </div>
                    </Route>

                    <Route path="/">
                        <div className="flex-1 p-6 md:p-12 text-center">
                            <h1 className="text-3xl font-bold mb-6 text-indigo-600">Find Your Mentor</h1>
                            {/* URL Input */}
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
                                        ref={swiperRef}
                                        slidesPerView={4}
                                        spaceBetween={20}
                                        loop={true}
                                        autoplay={{
                                            delay: 3000,
                                            disableOnInteraction: false,
                                        }}
                                        breakpoints={{
                                            640: {
                                                slidesPerView: 2,
                                            },
                                            768: {
                                                slidesPerView: 3,
                                            },
                                            1024: {
                                                slidesPerView: 4,
                                            },
                                        }}
                                    >
                                        {mentors.map((mentor, index) => (
                                            <SwiperSlide key={index}>
                                                <MentorCard mentor={mentor} />
                                            </SwiperSlide>
                                        ))}

                                        <div
                                            className="swiper-button-prev text-white absolute top-1/2 left-4 transform -translate-y-1/2 z-10 cursor-pointer"
                                            onClick={() => swiperRef.current.swiper.slidePrev()}
                                        >
                                            &lt;
                                        </div>
                                        <div
                                            className="swiper-button-next text-white absolute top-1/2 right-4 transform -translate-y-1/2 z-10 cursor-pointer"
                                            onClick={() => swiperRef.current.swiper.slideNext()}
                                        >
                                            &gt;
                                        </div>
                                    </Swiper>
                                )
                            )}
                        </div>
                    </Route>
                </Switch>
            </div>
        </Router>
    );
}

export default App;
