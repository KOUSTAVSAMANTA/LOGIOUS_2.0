import { useState,useRef } from "react";
import { BsSend } from "react-icons/bs";
import useSendMessage from "../../hooks/useSendMessage";
// import { BsSend } from 'react-icons/bs';
import { AiOutlinePicture, AiOutlineAudio } from 'react-icons/ai';

const MessageInput = () => {
	const [message, setMessage] = useState("");
	const { loading, sendMessage } = useSendMessage();
	const [audioBlob, setAudioBlob] = useState(null);
	const imageInput = useRef(null);
  	const audioInput = useRef(null);

	const handleSubmit = async (e) => {
		e.preventDefault();
		if (!message) return;
		await sendMessage(message);
		setMessage("");
	};

	const handleImageUpload = (file) => {
		// Add your image upload logic here
		const fileName = file.name;
  		console.log('Selected image file name:', fileName);
	  };
	
	  const handleAudioUpload = (file) => {
		// Add your audio upload logic here
	  };
	  const handleSendAudio = () => {
		// Handle sending audio logic here
	  };
	  const startRecording = () => {
		// Start recording logic
	  };
		

	return (
<form className='px-4 my-3' onSubmit={handleSubmit}>
      <div className='w-full relative flex items-center'>
        <input
          type='text'
          className='border text-sm rounded-lg block w-full p-2.5 bg-gray-700 border-gray-600 text-white flex-grow mr-2'
          placeholder='Send a message'
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        {/* <input
          type='file'
          accept='image/*'
          className='hidden'
          onChange={(e) => handleImageUpload(e.target.files[0])}
          ref={imageInput}
        />
        <button type='button' className='btn btn-ghost' onClick={() => imageInput?.current?.click()}>
          <AiOutlinePicture />
        </button>
        <input
          type='file'
          accept='audio/*'
          className='hidden'
          onChange={(e) => handleAudioUpload(e.target.files[0])}
          ref={audioInput}
        />
        <button type='button' className='btn btn-ghost' onClick={startRecording}>
          <AiOutlineAudio />
        </button> */}
        <button type='submit' className='btn btn-ghost'>
          {loading ? <div className='loading loading-spinner'></div> : <BsSend />}
        </button>
        {audioBlob && <button type='button' className='btn btn-ghost' onClick={handleSendAudio}>Send Audio</button>}
      </div>
    </form>

	);
};
export default MessageInput;

// STARTER CODE SNIPPET
// import { BsSend } from "react-icons/bs";

// const MessageInput = () => {
// 	return (
// 		<form className='px-4 my-3'>
// 			<div className='w-full'>
// 				<input
// 					type='text'
// 					className='border text-sm rounded-lg block w-full p-2.5  bg-gray-700 border-gray-600 text-white'
// 					placeholder='Send a message'
// 				/>
// 				<button type='submit' className='absolute inset-y-0 end-0 flex items-center pe-3'>
// 					<BsSend />
// 				</button>
// 			</div>
// 		</form>
// 	);
// };
// export default MessageInput;
