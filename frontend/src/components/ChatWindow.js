// import React, { useState, useEffect, useRef } from "react";
// import "./ChatWindow.css";
// import { getAIMessage } from "../api/api";
// import { marked } from "marked";

// function ChatWindow() {

//   const defaultMessage = [{
//     role: "assistant",
//     content: "Hi, how can I help you today?"
//   }];

//   const [messages,setMessages] = useState(defaultMessage)
//   const [input, setInput] = useState("");

//   const messagesEndRef = useRef(null);

//   const scrollToBottom = () => {
//       messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
//   };

//   useEffect(() => {
//       scrollToBottom();
//   }, [messages]);

//   const handleSend = async (input) => {
//     if (input.trim() !== "") {
//       // Set user message
//       setMessages(prevMessages => [...prevMessages, { role: "user", content: input }]);
//       setInput("");

//       // Call API & set assistant message
//       const newMessage = await getAIMessage(input);
//       setMessages(prevMessages => [...prevMessages, newMessage]);
//     }
//   };

//   return (
//       <div className="messages-container">
//           {messages.map((message, index) => (
//               <div key={index} className={`${message.role}-message-container`}>
//                   {message.content && (
//                       <div className={`message ${message.role}-message`}>
//                           <div dangerouslySetInnerHTML={{__html: marked(message.content).replace(/<p>|<\/p>/g, "")}}></div>
//                       </div>
//                   )}
//               </div>
//           ))}
//           <div ref={messagesEndRef} />
//           <div className="input-area">
//             <input
//               value={input}
//               onChange={(e) => setInput(e.target.value)}
//               placeholder="Type a message..."
//               onKeyPress={(e) => {
//                 if (e.key === "Enter" && !e.shiftKey) {
//                   handleSend(input);
//                   e.preventDefault();
//                 }
//               }}
//               rows="3"
//             />
//             <button className="send-button" onClick={handleSend}>
//               Send
//             </button>
//           </div>
//       </div>
// );
// }

// export default ChatWindow;
import React, { useState, useEffect, useRef } from "react";
import "./ChatWindow.css";
import { getAIMessage } from "../api/api";
import { marked } from "marked";

function ChatWindow() {
  // Default welcome message
  const defaultMessage = [
    {
      role: "assistant",
      content: "Hi, how can I help you today?"
    }
  ];

  const [messages, setMessages] = useState(defaultMessage);
  const [input, setInput] = useState(""); // ✅ input must always be a string
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when new messages appear
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // ✅ Simplified handleSend using component state directly
  const handleSend = async () => {
    if (!input || input.trim() === "") return;

    // Add user message
    setMessages((prev) => [...prev, { role: "user", content: input }]);
    const userInput = input;
    setInput("");

    try {
      // Call backend API for AI reply
      const newMessage = await getAIMessage(userInput);
      setMessages((prev) => [...prev, newMessage]);
    } catch (error) {
      console.error("Error fetching AI message:", error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "⚠️ Unable to reach backend." }
      ]);
    }
  };

  return (
    <div className="messages-container">
      {messages.map((message, index) => (
        <div key={index} className={`${message.role}-message-container`}>
          {message.content && (
            <div className={`message ${message.role}-message`}>
              <div
                dangerouslySetInnerHTML={{
                  __html: marked(message.content).replace(/<p>|<\/p>/g, "")
                }}
              ></div>
            </div>
          )}
        </div>
      ))}

      <div ref={messagesEndRef} />

      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          onKeyPress={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              handleSend();
              e.preventDefault();
            }
          }}
          rows="3"
        />
        <button className="send-button" onClick={handleSend}>
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatWindow;
