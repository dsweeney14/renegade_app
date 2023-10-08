import { useAuthContext } from "../authContext";
import { Navigate } from 'react-router-dom'

// This file will redirect the user to the login page when the refresh token expires

export const RequireAuth = ({children}) => {
    const auth = useAuthContext()
    const refreshToken = localStorage.getItem("refresh_token")

    if (!refreshToken) {
        return <Navigate to="/login" />
    }

    return children
}