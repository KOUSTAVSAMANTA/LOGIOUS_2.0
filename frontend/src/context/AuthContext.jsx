import { createContext, useContext, useState } from "react";

export const AuthContext = createContext();

// eslint-disable-next-line react-refresh/only-export-components
export const useAuthContext = () => {
	return useContext(AuthContext);
};

export const AuthContextProvider = ({ children }) => {
	const [authUser, setAuthUser] = useState(JSON.parse(localStorage.getItem("chat-user")) || null);
	const [Aitype, setAI] = useState("Assistant")
	const [Img,setImg] = useState("null")

	return <AuthContext.Provider value={{ authUser, setAuthUser,Aitype,setAI,Img,setImg }}>{children}</AuthContext.Provider>;
};
