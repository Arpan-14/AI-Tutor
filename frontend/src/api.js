import axios from 'axios';

// API_BASE_URL is the backend FastAPI server URL, not a model endpoint.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const sendChatMessage = async (message, userName, topic) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/chat`, {
      message,
      user_name: userName,
      topic,
    });
    return response.data.response;
  } catch (error) {
    console.error("❌ API Error:", error);
    return "❌ Failed to get response from AI Tutor.";
  }
};

export const fetchUserHistory = async (userName) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/history/${userName}`);
    return response.data;
  } catch (error) {
    console.error("❌ Fetch History Error:", error);
    return [];
  }
};

export const fetchUserStats = async (userName) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/users/${userName}/stats`);
    return response.data.statistics;
  } catch (error) {
    console.error("❌ Fetch Stats Error:", error);
    return {};
  }
};
