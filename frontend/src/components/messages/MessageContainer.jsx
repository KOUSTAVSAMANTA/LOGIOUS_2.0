import { useEffect, useState, useRef } from "react";
import useConversation from "../../zustand/useConversation";
import MessageInput from "./MessageInput";
import Messages from "./Messages";
import { TiMessages } from "react-icons/ti";
import { useAuthContext } from "../../context/AuthContext";
import "./msgcont.css"

const MessageContainer = () => {
	const { selectedConversation, setSelectedConversation } = useConversation();

	const { authUser,setAI, Aitype, Img, setImg } = useAuthContext();
	const [selectedValue, setSelectedValue] = useState('');
	const fileInputRef = useRef(null);

    const handleSelectChange = (event) => {
        setSelectedValue(event.target.value);
		setImg(event.target.value)
		console.log(selectedValue)
    };

	const handleFileChange = async () => {
		const file = fileInputRef.current.files[0];
		const fileName = file.name; // Get the file name

		const formData = new FormData();
		formData.append('file', file);

		try {
			const response = await fetch('http://127.0.0.1:8000/upload', {
				method: 'POST',
				body: formData
			});

			if (response.ok) {
				console.log('File uploaded successfully');
				// Handle success
			} else {
				console.error('File upload failed');
				// Handle error
			}
		} catch (error) {
			console.error('Error uploading file:', error);
			// Handle error
		}
		setImg(fileName)
		// console.log("selected",fileName)
	};


	function handleItemIMG(event) {
		const clickedItemText = event.target.innerText;
		if (clickedItemText === "Upload") {

			console.log(`Clicked item: ${clickedItemText}`, Img);
			document.getElementById('my_modal_1').showModal()
		} else {
			console.log(`Clicked item: ${clickedItemText}`, Img);
			document.getElementById('my_modal_2').showModal()
		}
		// Perform actions based on the clicked item
	}

	const clearmem = async ()=>{
		const res = await fetch('http://localhost:8000/clear/', {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({ 
						userID:selectedConversation._id+authUser._id
				 }),
				})
		const data = await res.json()
		alert(data.response)
	}


	const handleItemClick = () => {
		const newAIType = Aitype === "Assistant" ? "Chat" : "Assistant";
		console.log(newAIType)
		setAI(newAIType);
		// setDropdownOpen(false); // Close the dropdown after selecting an item
	};

	useEffect(() => {
		// cleanup function (unmounts)
		return () => setSelectedConversation(null);
	}, [setSelectedConversation]);

	const renderImgOption = () => {
        if (Img!==null && Img.trim() !== '' ) {
            return <option>{Img}</option>;
        }
    };
	console.log(Img)

	return (
		<div className='md:min-w-[450px] flex flex-col wrapper '>
			{!selectedConversation ? (
				<NoChatSelected />
			) : (
				<>
					{/* Header */}
					<div className='bg-slate-500 px-4 py-2 mb-2 flex items-center justify-between'>
						<div className='flex items-center'>
							<div className='w-12 rounded-full'>
								<img src={selectedConversation.profilePic} alt='user avatar' className="h-8" />
							</div>
							<span className='text-gray-900 font-bold'>{selectedConversation.fullName}</span>
						</div>
						<ul className="menu menu-vertical lg:menu-horizontal flex-row bg-base-200 rounded-box">
							<li><a onClick={handleItemIMG}>Upload</a></li>
							<li><a onClick={handleItemIMG}>Images</a></li>
							<li><a onClick={clearmem}>Clear AI Memory</a></li>
						</ul>
						<button className="btn  btn-outline btn-warning" onClick={handleItemClick}>{Aitype}</button>
					</div>
					<dialog id="my_modal_1" className="modal">
						<div className="modal-box">
							<h3 className="font-bold text-lg">Hello!</h3>
							<p className="py-4">Press ESC key or click the button below to close</p>
							<input
								type="file"
								className="file-input file-input-bordered w-full max-w-xs"
								ref={fileInputRef}
								onChange={handleFileChange}
							/>
							<div className="modal-action">
								<form method="dialog">
									{/* if there is a button in form, it will close the modal */}
									<button className="btn">Close</button>
								</form>
							</div>
						</div>
					</dialog>

					<dialog id="my_modal_2" className="modal">
						<div className="modal-box">
							<h3 className="font-bold text-lg">Hello!</h3>
							<p className="py-4">Press ESC key or click the button below to close</p>
							<p className="py-4">Currently Selected image is {Img}</p>
							<select className="select select-info w-full max-w-xs" value={selectedValue} onChange={handleSelectChange}>
								<option disabled selected>Select The Image </option>
								<option>null</option>
								{renderImgOption()}
							</select>
							<div className="modal-action">
								<form method="dialog">
									{/* if there is a button in form, it will close the modal */}
									<button className="btn">Close</button>
								</form>
							</div>
						</div>
					</dialog>


					<Messages />
					<MessageInput />
				</>
			)}
		</div>
	);
};
export default MessageContainer;

const NoChatSelected = () => {
	const { authUser } = useAuthContext();
	return (
		<div className='flex items-center justify-center w-full h-full'>
			<div className='px-4 text-center sm:text-lg md:text-xl text-gray-200 font-semibold flex flex-col items-center gap-2'>
				<p>Welcome 👋 {authUser.fullName} ❄</p>
				<p>Select a chat to start messaging</p>
				<TiMessages className='text-3xl md:text-6xl text-center' />
			</div>
		</div>
	);
};

// STARTER CODE SNIPPET
// import MessageInput from "./MessageInput";
// import Messages from "./Messages";

// const MessageContainer = () => {
// 	return (
// 		<div className='md:min-w-[450px] flex flex-col'>
// 			<>
// 				{/* Header */}
// 				<div className='bg-slate-500 px-4 py-2 mb-2'>
// 					<span className='label-text'>To:</span> <span className='text-gray-900 font-bold'>John doe</span>
// 				</div>

// 				<Messages />
// 				<MessageInput />
// 			</>
// 		</div>
// 	);
// };
// export default MessageContainer;
