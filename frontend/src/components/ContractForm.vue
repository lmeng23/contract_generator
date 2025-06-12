<template>
  <div class="contract-form-container">
    <el-card class="form-card">
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
          <el-select v-model="formData.deliveryMethod" placeholder="请选择运输方式" style="width: 100%;">
            <el-option label="双方协商" value="双方协商" />
            <el-option label="由甲方到乙方仓库自提货" value="由甲方到乙方仓库自提货" />
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
    </el-card>
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
  min-height: 100vh;
  min-height: calc(var(--vh, 1vh) * 100);
  width: 100%;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.form-card {
  width: 100%;
  max-width: 1400px;
  /* 原1200，已加大 */
  height: 100vh;
  height: calc(var(--vh, 1vh) * 100);
  margin: 0;
  border-radius: 0;
  overflow-y: auto;
}

.card-header {
  text-align: center;
  margin: 20px 0;
}

.card-header h2 {
  font-size: 24px;
  margin: 0;
  padding: 0;
}

.contract-form {
  padding: 20px;
  max-width: 1000px;
  /* 原800，已加大 */
  margin: 0 auto;
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
  /* 原120px，已加大 */
  text-align: right;
  font-weight: bold;
  white-space: nowrap;
  /* 防止换行 */
  overflow: hidden;
  text-overflow: ellipsis;
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
  /* 原500，已加大 */
  font-size: 20px;
  height: 50px;
  padding: 10px 20px;
}

@media (max-width: 768px) {
  .form-card {
    height: 100%;
    min-height: 100vh;
    min-height: calc(var(--vh, 1vh) * 100);
  }

  .contract-form {
    padding: 10px;
  }

  .card-header h2 {
    font-size: 20px;
  }

  :deep(.el-form-item) {
    flex-direction: row;
    margin-bottom: 25px;
  }

  :deep(.el-form-item__label) {
    flex: 0 0 110px;
    /* 原100，已加大 */
    padding-right: 10px;
    font-size: 14px;
    white-space: nowrap;
  }

  .submit-button {
    font-size: 18px;
    height: 45px;
    max-width: 600px;
    /* 保持一致 */
  }
}

@media (max-width: 480px) {
  .card-header {
    margin: 10px 0;
  }

  .contract-form {
    padding: 5px 10px;
  }

  :deep(.el-form-item) {
    margin-bottom: 20px;
  }

  :deep(.el-form-item__label) {
    flex: 0 0 100px;
    /* 原90，已加大 */
    font-size: 13px;
    white-space: nowrap;
  }

  .submit-button {
    font-size: 16px;
    height: 40px;
    max-width: 600px;
  }
}

:deep(.el-input__inner) {
  height: 38px !important;
  line-height: 38px;
  padding-top: 10px;
  padding-bottom: 10px;
}

@media (max-width: 768px) {
  :deep(.el-input__inner) {
    height: 38px !important;
    padding-top: 8px;
    padding-bottom: 8px;
  }
}

@media (max-width: 480px) {
  :deep(.el-input__inner) {
    height: 38px !important;
    padding-top: 7px;
    padding-bottom: 7px;
  }
}
</style>
