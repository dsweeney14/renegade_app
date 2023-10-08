import axios from "axios";


const auth = {
    isAuthenticated: false,
    accessToken: null
}

const setAccessToken = (token) => {
  auth.accessToken = token;
  auth.isAuthenticated = true;
};

const clearAccessToken = () => {
  auth.accessToken = null;
  auth.isAuthenticated = false;
};

const login = (username, password) => {
  return axios
    .post("/auth/login", { username, password })
    .then((response) => {
      const { access_token } = response.data;
      setAccessToken(access_token);
      return response;
    });
};

const logout = () => {
  clearAccessToken();
};

const authFetch = (url, options) => {
  const headers = {
    ...options.headers,
    Authorization: `Bearer ${auth.accessToken}`,
  };
  return axios(url, { ...options, headers });
};

export { auth, login, logout, authFetch };
