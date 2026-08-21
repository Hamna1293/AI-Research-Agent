import axios from "axios";

const API_URL = "http://127.0.0.1:8000";


const reportService = {

    getReport: async (filename) => {

        const response = await axios.get(
            `${API_URL}/report/${encodeURIComponent(filename)}`
        );

        return response.data;
    }

};


export default reportService;