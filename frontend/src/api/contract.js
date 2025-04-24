import axios from 'axios'

// 创建合同
export function generateContract(data) {
    const baseURL = import.meta.env.VITE_API_BASE_URL
    return axios.post(`${baseURL}/api/contract/generate`, data)
}
