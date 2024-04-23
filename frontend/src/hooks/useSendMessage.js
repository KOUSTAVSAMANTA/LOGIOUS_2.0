import { useState } from "react";
import useConversation from "../zustand/useConversation";
import toast from "react-hot-toast";
import { useAuthContext } from "../context/AuthContext";

const useSendMessage = () => {
	const [loading, setLoading] = useState(false);
	const { authUser } = useAuthContext();
	const { messages, setMessages, selectedConversation } = useConversation();

	const sendMessage = async (message) => {
		setLoading(true);
		try {
			console.log(message)
			if(message.includes("@logious")){
				console.log("AI",messages,selectedConversation._id,authUser._id)

				const res = await fetch('http://localhost:8000/predict/', {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({ 
						text: message.replace("@logious","logious"),
						userID:selectedConversation._id+authUser._id
				 }),
				})
				const data = await res.json()
				console.log(data)
				let msg ={createdAt:new Date().toISOString(),
					message:data.response,
					receiverId:selectedConversation._id,
					senderId:authUser._id}
				setMessages([...messages, msg]);
			}else{
				console.log("user")
				const res = await fetch(`/api/messages/send/${selectedConversation._id}`, {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({ message }),
				});
				const data = await res.json();
				if (data.error) throw new Error(data.error);
	
				setMessages([...messages, data]);
			}
		} catch (error) {
			toast.error(error.message);
		} finally {
			setLoading(false);
		}
	};

	return { sendMessage, loading };
};
export default useSendMessage;
