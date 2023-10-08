import { useNavigate } from "react-router-dom"

// This file contains the logout functionality

const UseLogout = () => {
    const navigate = useNavigate()

    const logout = () => {
        localStorage.removeItem("refresh_token")
        navigate('/login')
    };

    return logout;
};

export default UseLogout;