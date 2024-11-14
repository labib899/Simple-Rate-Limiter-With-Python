import React, { useState } from "react";
import axios from "axios";

function App() {
  const [response, setResponse] = useState("");
  const [rateLimitInfo, setRateLimitInfo] = useState(null);

  const sendRequest = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/data");
      
      setResponse(res.data.message || "Request successful");
      setRateLimitInfo({
        limit: res.headers["x-ratelimit-limit"],
        remaining: res.headers["x-ratelimit-remaining"],
        retryAfter: res.headers["x-ratelimit-retry-after"],
      });
    } catch (err) {
      if (err.response?.status === 429) {
        console.log(err.response.headers);
        setResponse(err.response?.data?.detail || "Rate limit exceeded");
        const retryAfter = err.response?.headers["x-ratelimit-retry-after"];
        setRateLimitInfo({
          limit: err.response?.headers["x-ratelimit-limit"],
          remaining: err.response?.headers["x-ratelimit-remaining"],
          retryAfter: retryAfter ? `${retryAfter} seconds` : "Unknown time",
        });
      } else {
        setResponse("Error occurred");
        setRateLimitInfo(null);
      }
    }
  };

  return (
    <div className="App">
      <h1>Rate Limiter Demo</h1>
      <button onClick={sendRequest}>Send Request</button>
      <p><strong>Response:</strong> {response}</p>

      {rateLimitInfo && (
        <div className="rate-limit-info">
          <h3>Rate Limit Information:</h3>
          <p><strong>Limit:</strong> {rateLimitInfo.limit || "N/A"}</p>
          <p><strong>Remaining:</strong> {rateLimitInfo.remaining || "N/A"}</p>
          {rateLimitInfo.retryAfter && response=='Rate limit exceeded' && (
            <p><strong>Retry After:</strong> {rateLimitInfo.retryAfter}</p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
