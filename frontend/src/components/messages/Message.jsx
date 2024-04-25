import { useAuthContext } from "../../context/AuthContext";
import { extractTime } from "../../utils/extractTime";
import useConversation from "../../zustand/useConversation";

const Message = ({ message }) => {
	const { authUser } = useAuthContext();
	const { selectedConversation } = useConversation();
	const fromMe = message.senderId === authUser._id;
	const formattedTime = extractTime(message.createdAt);
	// const chatClassName = fromMe ? "chat-end" : "chat-start";
	const chatClassName = message.senderId === 'AI' ? 'chat-start' : (fromMe ? 'chat-end' : 'chat-start');
	let unc = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRF63g8BlJpwHJ-YQvMnOa70YWk-suGXzjA_A&s'
	const profilePic = message.senderId==='AI'?unc:(fromMe ? authUser.profilePic : selectedConversation?.profilePic);
	const bubbleBgColor = message.senderId==='AI'?'bg-green-500':(fromMe ? "bg-blue-500" : "");

	const shakeClass = message.shouldShake ? "shake" : "";

	return (
		<div className={`chat ${chatClassName}`}>
			<div className='chat-image avatar'>
				<div className='w-10 rounded-full'>
					<div className="w-10 rounded-full">
					<img alt='Tailwind CSS chat bubble component' src={profilePic} /></div>
				</div>
			</div>
			<div className={`chat-bubble text-white ${bubbleBgColor} ${shakeClass} pb-2`}>{message.message}</div>
			<div className='chat-footer opacity-50 text-xs flex gap-1 items-center'>{formattedTime}</div>
		</div>
	);
};
export default Message;
