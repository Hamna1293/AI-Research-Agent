import api from "../api/axios";

export async function askAI(question) {

    const response = await api.post("/chat", {

        question,

        top_k: 5,

    });

    return response.data.answer;

}