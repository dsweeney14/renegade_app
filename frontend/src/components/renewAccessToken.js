import axios from 'axios';

// This component generated a new access token when the refresh token is not expired

const renewAccessToken = (refreshToken) => {
    return new Promise((resolve, reject) => {
        axios
        .post("auth/refresh", {refresh_token: refreshToken})
        .then((response) => {
            const { access_token } = response.data;
            resolve(access_token)
        })
        .catch((error) => {
            reject(error)
        })
    })
}

export default renewAccessToken;