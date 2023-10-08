import { useState, useContext, createContext, useEffect } from "react";
import jwt_decode from 'jwt-decode';
import renewAccessToken from './components/renewAccessToken'


// This file is used to give authentication context for access control

const AuthContext = createContext(null)

export const AuthProvider = ({children}) => {
  const [logged, setLogged] = useState(false)
  const [accessToken, setAccessToken] = useState(null)
  const [refreshToken, setRefreshToken] = useState(null)

  const loginContext = (access_token, refresh_token) => {
    setLogged(true)
    setAccessToken(access_token)
    setRefreshToken(refresh_token)
    localStorage.setItem("refresh_token", refresh_token)
  }

  const logoutContext = () => {
    setLogged(false)
    setAccessToken(null)
    setRefreshToken(null)
  }

  useEffect( () => {
    const TokenExpired = () => {
      if(!refreshToken) return true;
      const decodedToken = jwt_decode(refreshToken);
      const currentTime = Date.now() / 1000;
      return decodedToken.exp < currentTime;
    }
    if (TokenExpired()) {
      renewAccessToken(refreshToken)
      .then((newAccessToken) => {
        setAccessToken(newAccessToken);
      })
      .catch(() => {
        logoutContext();
      })
    }
  }, [refreshToken, setAccessToken, logoutContext])

  return <AuthContext.Provider value={{ logged, accessToken, refreshToken, loginContext, logoutContext }}>
    {children}
  </AuthContext.Provider>
}

export const useAuthContext = () => {
    return useContext(AuthContext)
}