import '../App.css';
import React, {useState, useEffect} from 'react'
/*
TODO: randomized banner message
Periodically, swap Banner message from a collection of banner messages that bestow financial knowledge from known historical figures

Swap every 1.5 minutes, fade out and fade in
*/

/*
1 Load currently stored 3 messages (on new user, use hard coded, if returning use cached),
2 then fetch the daily messages from DB.
3 Update list of messages with new list of dailies. (actual list would be more than 3, but keeping cache footprint small)
4 Store 3 new random messages to cache
*/
const adviceBanner = {
  message: "Past Performance is Not Indicative of Future Results",
  author: "Common Finance Mantra"
}

interface Message {
  author: string;
  message: string;
}

const BannerMessage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);

  // Function to fetch messages from the API
  const fetchMessages = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/v1/daily_messages");
      if (response.ok) {
        const data: Message[] = await response.json();
        setMessages(data); // Update messages state with new fetched messages
        cacheMessages(data); // Cache 3 random messages
      } else {
        console.error('Failed to fetch messages');
      }
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  // Function to cache messages in localStorage
  const cacheMessages = (messages: Message[]) => {
    const cachedMessages = messages.slice(0, 3); // Select first 3 random messages
    localStorage.setItem('cachedMessages', JSON.stringify(cachedMessages));
  };

  useEffect(() => {
    // Check if there are cached messages, if not, fetch new ones
    const cached = localStorage.getItem('cachedMessages');
    if (cached) {
      setMessages(JSON.parse(cached));
    } else {
      fetchMessages();
    }
  }, []); // Empty dependency array ensures this runs only on initial load

  // JSX to display messages
  return (
    <div>
      <i>
  <h2>{adviceBanner.message}</h2>
  {/* <h3>- {adviceBanner.author}</h3> */}
</i>
      <h2>Messages</h2>
      <ul>
        {messages.map((message, index) => (
          <li key={index}>
            <strong>{message.author}: </strong>
            {message.message}
          </li>
        ))}
      </ul>
    </div>

  );
};

export default BannerMessage;