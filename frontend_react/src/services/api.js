import axios from 'axios';

const API_URL = 'http://192.168.0.110:5000/predict';  // Your Flask backend endpoint

export const getAnswer = async (question) => {
    try {
        const response = await axios.post(API_URL, { question });
        return response.data.response;
    } catch (error) {
        console.error("Error fetching the answer:", error);
        throw error;
    }
};
