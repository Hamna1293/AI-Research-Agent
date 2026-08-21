const CHAT_STORAGE_KEY = "research_assistant_chat";


export function loadChatHistory() {

    try {

        const savedChat = localStorage.getItem(
            CHAT_STORAGE_KEY
        );


        if (!savedChat) {

            return [
                {
                    role: "ai",
                    text: "Hello! 👋 Upload research papers and ask me anything about them."
                }
            ];

        }


        const parsedChat = JSON.parse(savedChat);


        if (!Array.isArray(parsedChat)) {

            return [
                {
                    role: "ai",
                    text: "Hello! 👋 Upload research papers and ask me anything about them."
                }
            ];

        }


        return parsedChat;

    }

    catch (error) {

        console.error(
            "Failed to load chat history:",
            error
        );


        return [
            {
                role: "ai",
                text: "Hello! 👋 Upload research papers and ask me anything about them."
            }
        ];

    }

}


export function saveChatHistory(messages) {

    try {

        localStorage.setItem(
            CHAT_STORAGE_KEY,
            JSON.stringify(messages)
        );

    }

    catch (error) {

        console.error(
            "Failed to save chat history:",
            error
        );

    }

}


export function clearChatHistory() {

    try {

        localStorage.removeItem(
            CHAT_STORAGE_KEY
        );

    }

    catch (error) {

        console.error(
            "Failed to clear chat history:",
            error
        );

    }

}