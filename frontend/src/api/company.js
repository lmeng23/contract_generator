import axios from 'axios';  // 直接用axios

const url = import.meta.env.VITE_API_BASE_URL
const baseURL = ` ${url}/api/company`


// 搜索公司（模糊匹配）
export function suggestCompanies(keyword) {
    return axios.get(`${baseURL}/suggest`, {
        params: { keyword }
    });
}

// 根据ID获取公司详情
export function getCompany(companyId) {
    return axios.get(`${baseURL}/${companyId}`);
}

// 创建公司
export function createCompany(data) {
    return axios.post(`${baseURL}/create`, data);
}

// 更新公司
export function updateCompany(companyId, data) {
    return axios.put(`${baseURL}/${companyId}`, data);
}
