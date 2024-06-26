import axios from 'axios';

// set the default base url for axios requests
const API_SERVER = import.meta.env.VITE_API_SERVER;
axios.defaults.baseURL = API_SERVER;
axios.defaults.withCredentials = true;

// Source code: https://stackoverflow.com/a/15724300
export function getTokenFromCookie() {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; access_token=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

let access_token = getTokenFromCookie();
if (access_token !== undefined) {
    axios.defaults.headers.common['Authorization'] = access_token;
}

export default
    class APIClient {
    /**
     * Get all the categories with current IQ in each category
     * (keys are category id)
     * @returns {Array} {category_id: {category_name: String, user_iq: Number}}
     */
    static async getCategories() {
        const response = await axios.get(`/api/category/iq/`);
        return response.data;
    }

    /**
     * 
     * @param {Number} category_id 
     * @returns {String} category name
     */
    static async getCategoryName(category_id) {
        const response = await axios.get(`/api/category/${category_id}/name`);
        return response.data.category_name;
    }

    /**
     * Get a new question for a given category
     * @param {Number} category_id 
     * @returns {String} question text
     */
    static async getNewQuestion(category_id) {
        const response = await axios.get(`/api/question/${category_id}/new`);
        return response.data.text;
    }

    /**
     * Get if the user has already asked for options
     * @returns {Boolean} true if options have been asked, false otherwise
     */
    static async getIfOptionsAsked(category_id) {
        const response = await axios.get(`/api/question/${category_id}/options_asked`);
        return !!response.data.options_asked;
    }

    /**
     * Get the options for the current question
     * @returns {Object} {"id_option": "text_option"}
     */
    static async getOptions(category_id) {
        const response = await axios.get(`/api/question/${category_id}/options`);
        return response.data.options;
    }

    /**
     * Return the image for a given category id
     * @param {Number} category_id 
     * @returns {String} base64 image {data:image/jpeg;base64, ...}
     */
    static async getImageCategory(category_id) {
        const arrayBufferToBase64 = (buffer) => {
            let binary = '';
            const bytes = new Uint8Array(buffer);
            const len = bytes.byteLength;
            for (let i = 0; i < len; i++) {
                binary += String.fromCharCode(bytes[i]);
            }
            return btoa(binary);
        }
        const response = await axios.get(`/api/category/${category_id}/image/`,
            {
                responseType: 'arraybuffer'
            });
        return 'data:image/jpeg;base64,' + arrayBufferToBase64(response.data);
    }

    /**
     * Get the current user IQ. It's the best players average IQ in all categories
     * @returns {Number} user IQ
     */
    static async getUserIQ(category_id) {
        const response = await axios.get(`/api/category/${category_id}/user_iq`);
        return response.data.user_iq;
    }

    /**
     * Get the global leaderboard. It's the best players average IQ in all categories
     * @returns {Array} [{user_id: Number, user_name: String, user_score: Number}]
     */
    static async getGlobalLeaderboard() {
        const response = await axios.get(`/api/rank/global_leaderboard/`);
        return response.data;
    }
    /**
     * Get the global leaderboard specific to a category. It's the players with the best IQ in this category id
     * @returns {Array} [{user_id: Number, user_name: String, user_score: Number}]
     */
    static async getCategoryLeaderboard(category_id) {
        const response = await axios.get(`/api/rank/${category_id}/leaderboard/`);
        return response.data;
    }

    /**
     * Get the global user rank based on average IQ in all categories of the connected player
     * @returns {Object} {user_rank: Number, user_score: Number}
     */
    static async getGlobalUserRank() {
        const response = await axios.get(`/api/rank/global_user/`);
        return response.data;
    }

    /**
     * Get the user rank specific to a category.
     * @returns {Object} {user_rank: Number, user_score: Number}
     */
    static async getCategoryUserRank(category_id) {
        const response = await axios.get(`/api/rank/${category_id}/user/`);
        return response.data;
    }

    /**
     * Post the answer to the question as a text
     * @param {String} answer_text 
     * @returns {Object} {user_is_correct: Boolean, right_answer: String, answer_sent: String} 
     */
    static async postAnswerText(answer_text, category_id) {
        const response = await axios.post(`/api/question/${category_id}/answer_text/`, {
            answer: answer_text,
        });
        return response.data;
    }

    /**
     * Post the answer to the question as an options
     * @param {String} option_id 
     * @returns {Object} {user_is_correct: Boolean, right_answer: String, answer_sent: String} 
     */
    static async postAnswerOption(option_id, category_id) {
        const response = await axios.post(`/api/question/${category_id}/answer_option/`, {
            answer: option_id,
        });
        return response.data;
    }

    /**
     * Register a new user
     * @param {String} username The username of the new user
     * @param {String} password The password of the new user
     * @returns {Object} Axios response type object
     */
    static async registerUser(username, password) {
        let response = await axios.post('/api/user/register/', {
            username: username,
            password: password
        });

        if (response.status === 201) {
            // register ok, login the user
            response = await this.loginUser(username, password);
        }
        return response;
    }

    /**
     * Log in an existing user
     * @param {String} username The username of the user
     * @param {String} password The password of the user
     * @returns {Object} Axios response type object
     */
    static async loginUser(username, password) {
        const response = await axios.post('/api/user/token/', {
            username: username,
            password: password
        });

        // set the token in the axios headers
        if (response.status === 200) {
            // set cookie
            let date = new Date(response.data.expires).toUTCString()
            document.cookie = `access_token=Token ${response.data.token};expires=${date};SameSite=Strict;Secure;`; // TODO adding expires date from backend

            // set axios header
            axios.defaults.headers.common['Authorization'] = "Token " + response.data.token;
        }

        return response;
    }

    /**
     * Post a new community question to the API.
     * @param {String} question - The text of the new question.
     * @param {Array<String>} options - An array of options for the question.
     * @returns {Object} {"text": String, "category": String }
     */
    static async postNewCommunityQuestion(question, options) {
        const
            response = await axios.post(`/api/question/new_community/`, {
                question,
                options,
                answer: '0'
            });
        return response.data;
    }

    /**
     * Log out an existing user
     * @returns {Object} The response data from the API
     */
    static async logoutUser() {
        // remove cookie
        document.cookie = `access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC;`;

        // remove axios header
        delete axios.defaults.headers.common['Authorization'];

        return { message: "User logged out" };
    }
}

