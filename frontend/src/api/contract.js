import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL

// 创建合同
export function generateContract(data) {
    return axios.post(`${baseURL}/api/contract/generate`, data)
}
