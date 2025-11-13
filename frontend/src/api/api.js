
// export const getAIMessage = async (userQuery) => {

//   const message = 
//     {
//       role: "assistant",
//       content: "Connect your backend here...."
//     }

//   return message;
// };
// frontend/src/app.js

// frontend/src/api/api.js

export const getAIMessage = async (userQuery) => {
  try {
    
    const response = await fetch("http://localhost:8001/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: userQuery }),
    });

    const data = await response.json();

    return {
      role: "assistant",
      content: data.message || "No response from backend",
    };
  } catch (error) {
    console.error("Error connecting to backend:", error);
    return {
      role: "assistant",
      content: "Error: Unable to reach backend. Please check if FastAPI is running.",
    };
  }
};
