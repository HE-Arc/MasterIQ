import axios from 'axios';

// set the default base url for axios requests
const API_SERVER = import.meta.env.VITE_API_SERVER;
axios.defaults.baseURL = API_SERVER;
axios.defaults.withCredentials = true;

export default
class APIClient {
    /**
     * Get all the categories with current IQ in each category
     * (keys are category id)
     * @returns 
     */
    static async getCategories()
    {
        const response = await axios.get(`/api/category/iq/`);
        return response.data;
    }
}