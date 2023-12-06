import React, { useState } from "react";

function NewMessage({ currentUser, onAddMessage }) {
  const [body, setBody] = useState("");

  function handleSubmit(e) {
    e.preventDefault();

    fetch("http://127.0.0.1:5555/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: currentUser.username,
        body: body,
      }),
    })
      .then((r) => {
        // Check for a successful response (status code 200: OK)
        if (r.ok) {
          return r.json();
        }
        // Throw an error for non-OK responses
        throw new Error("Failed to create a new message");
      })
      .then((newMessage) => {
        // Invoke the onAddMessage function to update the app with the new message
        onAddMessage(newMessage);
        // Reset the input field after a successful submission
        setBody("");
      })
      .catch((error) => {
        // Handle errors from fetch
        console.error(error.message);
      });
  }

  return (
    <form className="new-message" onSubmit={handleSubmit}>
      <input
        type="text"
        name="body"
        autoComplete="off"
        value={body}
        onChange={(e) => setBody(e.target.value)}
      />
      <button type="submit">Send</button>
    </form>
  );
}

export default NewMessage;
