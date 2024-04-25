import { useAuthContext } from "../../context/AuthContext";
import Conversations from "./Conversations";
import LogoutButton from "./LogoutButton";
import SearchInput from "./SearchInput";

const Sidebar = () => {
	const { authUser } = useAuthContext();

	return (
		<div className="flex-col border-r-1 shadow-right">
		<div className='bg-slate-500 h-16 w-50 border-r border-slate-400 mb-2 p-4 flex justify-between items-center'>
		  <img alt='Profile' src={authUser.profilePic} className="h-8 w-8 rounded-full" />
		  <LogoutButton />
		</div>
		<div className='border-r border-slate-500 p-4 flex flex-col'>
		  <SearchInput />
		  <div className='divider px-3'></div>
		  <Conversations />
		</div>
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
