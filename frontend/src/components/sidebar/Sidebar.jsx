import Conversations from "./Conversations";
import LogoutButton from "./LogoutButton";
import SearchInput from "./SearchInput";

const Sidebar = () => {
	return (

		<div className='border-r border-slate-500 p-4 flex flex-col'>
			{/* <div className='bg-slate-500 h-12 border-r border-slate-400 mb-2 flex'>
				
			</div> */}
			<SearchInput />
			<div className='divider px-3 '></div>
			<Conversations  />
			<LogoutButton />
		</div>
	);
};
export default Sidebar;

// STARTER CODE FOR THIS FILE
// import Conversations from "./Conversations";
// import LogoutButton from "./LogoutButton";
// import SearchInput from "./SearchInput";

// const Sidebar = () => {
// 	return (
// 		<div className='border-r border-slate-500 p-4 flex flex-col'>
// 			<SearchInput />
// 			<div className='divider px-3'></div>
// 			<Conversations />
// 			<LogoutButton />
// 		</div>
// 	);
// };
// export default Sidebar;
