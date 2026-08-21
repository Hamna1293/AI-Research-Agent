import { useState } from "react";
import { Send, Sparkles } from "lucide-react";

import { askAI } from "../services/chatService";

import {
    loadChatHistory,
    saveChatHistory
} from "../services/chatStorage";


function ChatBox() {

    const [messages, setMessages] = useState(
        () => loadChatHistory()
    );

    const [input, setInput] = useState("");

    const [loading, setLoading] = useState(false);


    const sendMessage = async () => {

        if (!input.trim() || loading) {
            return;
        }


        const question = input.trim();


        const userMessage = {
            role: "user",
            text: question,
        };


        const messagesWithUser = [
            ...messages,
            userMessage,
        ];


        setMessages(messagesWithUser);

        saveChatHistory(messagesWithUser);

        setInput("");

        setLoading(true);


        try {

            const answer = await askAI(question);


            const aiMessage = {
                role: "ai",
                text: answer,
            };


            const updatedMessages = [
                ...messagesWithUser,
                aiMessage,
            ];


            setMessages(updatedMessages);

            saveChatHistory(updatedMessages);

        }

        catch (error) {

            console.error(
                "Chat error:",
                error
            );


            const errorMessage = {
                role: "ai",
                text: "❌ Unable to connect to the AI backend.",
            };


            const updatedMessages = [
                ...messagesWithUser,
                errorMessage,
            ];


            setMessages(updatedMessages);

            saveChatHistory(updatedMessages);

        }

        finally {

            setLoading(false);

        }

    };


    return (

        <div className="chat-container">

            <div className="chat-messages">

                {
                    messages.map((msg, index) => (

                        <div
                            key={index}
                            className={
                                msg.role === "ai"
                                    ? "message ai-message"
                                    : "message user-message"
                            }
                        >

                            {
                                msg.role === "ai" && (
                                    <Sparkles size={16} />
                                )
                            }

                            <span>
                                {msg.text}
                            </span>

                        </div>

                    ))
                }


                {
                    loading && (

                        <div className="message ai-message">

                            <Sparkles size={16} />

                            <span>
                                AI is thinking...
                            </span>

                        </div>

                    )
                }

            </div>


            <div className="chat-input">

                <input
                    type="text"
                    value={input}
                    placeholder="Ask anything about your uploaded research..."
                    onChange={(event) => {
                        setInput(event.target.value);
                    }}
                    onKeyDown={(event) => {

                        if (
                            event.key === "Enter" &&
                            !event.shiftKey
                        ) {

                            event.preventDefault();

                            sendMessage();

                        }

                    }}
                    disabled={loading}
                />


                <button
                    type="button"
                    onClick={sendMessage}
                    disabled={
                        loading ||
                        !input.trim()
                    }
                >

                    <Send size={18} />

                </button>

            </div>

        </div>

    );

}


export default ChatBox;