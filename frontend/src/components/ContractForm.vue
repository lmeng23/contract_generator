<template>
  <div class="contract-form-container">
    <el-form ref="formRef" :model="formData" :rules="rules" label-width="120px" class="contract-form">
      <el-form-item label="合同编号:" prop="contractNumber">
        <el-input v-model="formData.contractNumber" />
      </el-form-item>

      <el-form-item label="签订日期:" prop="signingDate">
        <el-date-picker v-model="formData.signingDate" type="date" placeholder="选择日期" format="YYYY-MM-DD"
          value-format="YYYY-MM-DD" style="width: 100%;" />
      </el-form-item>

      <el-form-item label="商品吨位:" prop="productTonnage">
        <el-input v-model="formData.productTonnage" />
      </el-form-item>

      <el-form-item label="商品单价:" prop="unitPrice">
        <el-input v-model="formData.unitPrice" />
      </el-form-item>

      <el-form-item label="优惠价格:">
        <el-input v-model="formData.specialPrice" placeholder="不优惠留空" />
      </el-form-item>

      <el-form-item label="公司名称:" prop="companyName">
        <el-autocomplete v-model="formData.companyName" :fetch-suggestions="fetchSuggestions"
          placeholder="输入公司名称，自动补全相关信息 " :trigger-on-focus="false" @select="handleSelectCompany" value-key="name"
          clearable />
      </el-form-item>

      <el-form-item label="电话号码:" prop="phoneNumber">
        <el-input v-model="formData.phoneNumber" />
      </el-form-item>

      <el-form-item label="公司地址:" prop="companyAddress">
        <el-input v-model="formData.companyAddress" />
      </el-form-item>

      <el-form-item label="纳税人识别号:" prop="taxId">
        <el-input v-model="formData.taxId" />
      </el-form-item>

      <el-form-item label="开户行地址:" prop="bankAddress">
        <el-input v-model="formData.bankAddress" />
      </el-form-item>

      <el-form-item label="银行账号:" prop="bankAccount">
        <el-input v-model="formData.bankAccount" />
      </el-form-item>

      <el-form-item label="运输方式:">
        <el-select v-model="formData.deliveryMethod" placeholder="请选择运输方式" style="width: 100%;" clearable filterable allow-create>
          <el-option label="双方协商" value="双方协商" />
          <el-option label="由甲方到乙方仓库自提货" value="由甲方到乙方仓库自提货" />
          <el-option label="乙方送到" value="乙方送到" />
        </el-select>
      </el-form-item>

      <el-form-item label="法人代表:">
        <el-input v-model="formData.legalRepresentative" placeholder="默认不填写" />
      </el-form-item>

      <el-form-item label="授权代理人:">
        <el-input v-model="formData.authorizedAgent" placeholder="默认不填写" />
      </el-form-item>

      <el-form-item class="submit-container">
        <el-button type="primary" class="submit-button" @click="submitForm">提交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { generateContract } from '@/api/contract'
import { suggestCompanies, createCompany, updateCompany } from '@/api/company'

const formData = reactive({
  contractNumber: '',
  signingDate: '',
  productTonnage: '',
  unitPrice: '',
  specialPrice: '',
  companyName: '',
  phoneNumber: '',
  companyAddress: '',
  taxId: '',
  bankAddress: '',
  bankAccount: '',
  deliveryMethod: '双方协商',
  legalRepresentative: '',
  authorizedAgent: '',
})

const formRef = ref(null)
const selectedCompanyId = ref(null)

// 验证规则
const rules = reactive({
  contractNumber: [
    { required: true, message: '请输入合同编号', trigger: 'blur' },
    { pattern: /^\d+$/, message: '合同编号必须是数字', trigger: 'blur' }
  ],
  signingDate: [
    { required: true, message: '请输入签订日期', trigger: 'blur' },
  ],
  productTonnage: [
    { required: true, message: '请输入商品吨位', trigger: 'blur' },
    { pattern: /^[0-9]+(\.[0-9]+)?$/, message: '商品吨位必须是数字(整数或小数)', trigger: 'blur' }
  ],
  unitPrice: [
    { required: true, message: '请输入商品单价', trigger: 'blur' },
    { pattern: /^[0-9]+$/, message: '商品单价必须是整数', trigger: 'blur' }
  ],
  companyName: [
    { required: true, message: '请输入公司名称', trigger: 'blur' }
  ],
  taxId: [
    { required: true, message: '请输入纳税人识别号', trigger: 'blur' }
  ],
  bankAddress: [
    { required: true, message: '请输入开户行地址', trigger: 'blur' }
  ],
  bankAccount: [
    { required: true, message: '请输入银行账号', trigger: 'blur' }
  ],
})

// 清洗输入数据（去除所有字符串的前后空格）
const trimFormData = () => {
  for (const key in formData) {
    if (typeof formData[key] === 'string') {
      formData[key] = formData[key].replace(/\s+/g, '');
    }
  }
}

const fetchSuggestions = async (queryString, cb) => {
  if (!queryString.trim()) {
    cb([])
    return
  }
  try {
    const res = await suggestCompanies(queryString)
    const companies = res.data || []
    cb(companies)
  } catch (error) {
    console.error('搜索公司失败:', error)
    cb([])
  }
}

// 选择建议公司时自动填充
const handleSelectCompany = (company) => {
  formData.companyName = company.name
  formData.phoneNumber = company.phone || ''
  formData.companyAddress = company.address || ''
  formData.taxId = company.tax_id || ''
  formData.bankAddress = company.bank_address || ''
  formData.bankAccount = company.bank_account || ''
  formData.legalRepresentative = company.legal_person || ''
  formData.authorizedAgent = company.agent || ''
  selectedCompanyId.value = company.id || null
}

// 表单提交逻辑
const submitForm = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) {
      ElMessage.error('请完善必填信息后再提交！')
      return
    }

    // 去除空格
    trimFormData()

    // 准备请求体（避免重复构造）
    const companyPayload = {
      name: formData.companyName,
      phone: formData.phoneNumber,
      address: formData.companyAddress,
      tax_id: formData.taxId,
      bank_address: formData.bankAddress,
      bank_account: formData.bankAccount,
      legal_person: formData.legalRepresentative,
      agent: formData.authorizedAgent
    }

    try {
      if (selectedCompanyId.value) {
        await updateCompany(selectedCompanyId.value, companyPayload)
      } else {
        await createCompany(companyPayload)
      }

      const res = await generateContract(formData)
      if (res.data.status === 'success') {
        ElMessage.success('合同生成成功！')
        const baseURL = import.meta.env.VITE_API_BASE_URL
        window.open(`${baseURL}/static/pdf/${res.data.filename}.pdf`, '_self')
      } else {
        ElMessage.warning('生成失败，请检查输入内容')
      }
    } catch (error) {
      console.error(error)
      ElMessage.error('提交失败，请检查输入内容！')
    }
  })
}
</script>

<style scoped>
.contract-form-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  height: 100vh;
  width: 100vw;
  margin: 0;
  padding: 0;
  overflow-y: auto;
  box-sizing: border-box;
}

.contract-form {
  width: 100%;
  padding: 40px 60px;
  box-sizing: border-box;
}

:deep(.el-form-item__content) {
  margin-left: 0 !important;
}

:deep(.el-form-item) {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
}

:deep(.el-form-item__label) {
  flex: 0 0 130px;
  text-align: right;
  font-weight: bold;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-right: 12px;
}

:deep(.el-form-item__content) {
  flex: 1;
  min-width: 0;
}

.submit-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.submit-button {
  width: 100%;
  max-width: 600px;
  font-size: 20px;
  height: 50px;
  padding: 10px 20px;
}

/* 平板设备 */
@media (max-width: 768px) {
  .contract-form {
    padding: 20px;
  }

  :deep(.el-form-item__label) {
    flex: 0 0 120px;
    font-size: 14px;
    margin-right: 10px;
  }

  .submit-button {
    font-size: 18px;
    height: 45px;
  }
}

/* 手机设备 */
@media (max-width: 480px) {
  .contract-form {
    padding: 15px 10px;
  }

  :deep(.el-form-item) {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
  }

  :deep(.el-form-item__label) {
    flex: 0 0 auto;
    min-width: 80px;
    max-width: 35%;
    text-align: right;
    margin-right: 8px;
    font-size: 13px;
    font-weight: bold;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  :deep(.el-form-item__content) {
    flex: 1;
    min-width: 0;
  }

  .submit-button {
    font-size: 16px;
    height: 40px;
  }
}

/* 超小屏幕设备 */
@media (max-width: 375px) {
  .contract-form {
    padding: 10px 8px;
  }

  :deep(.el-form-item__label) {
    font-size: 13px;
  }
}

:deep(.el-input__inner) {
  height: 38px !important;
  line-height: 38px;
  padding-top: 10px;
  padding-bottom: 10px;
}

/* 确保输入框在所有设备上都能完整显示 */
:deep(.el-input),
:deep(.el-select),
:deep(.el-date-editor) {
  width: 100%;
  max-width: 100%;
}

/* 自动完成组件的特殊处理 */
:deep(.el-autocomplete) {
  width: 100%;
}
</style>
