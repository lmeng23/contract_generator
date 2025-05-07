<template>
  <div class="contract-form-container">
    <el-card class="form-card">
      <div class="card-header">
        <h2>合同生成器</h2>
      </div>

      <el-form ref="formRef" :model="formData" :rules="rules" label-width="120px" class="contract-form">
        <el-form-item label="合同编号:" prop="contractNumber">
          <el-input v-model="formData.contractNumber" />
        </el-form-item>

        <el-form-item label="签订日期:" prop="signingDate">
          <el-date-picker v-model="formData.signingDate" type="date" placeholder="选择日期" format="YYYY-MM-DD"
            value-format="YYYY-MM-DD" style="width: 100%;" />
        </el-form-item>


        <el-form-item label="公司名称:" prop="companyName">
          <el-autocomplete v-model="formData.companyName" :fetch-suggestions="fetchSuggestions"
            placeholder="输入公司名称，自动补全相关信息 " :trigger-on-focus="true" @select="handleSelectCompany" value-key="name"
            clearable />
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

        <el-form-item label="电话号码:" prop="phoneNumber">
          <el-input v-model="formData.phoneNumber" />
        </el-form-item>

        <el-form-item label="公司地址:" prop="companyAddress">
          <el-input v-model="formData.companyAddress" />
        </el-form-item>

        <el-form-item label="法人代表:">
          <el-input v-model="formData.legalRepresentative" placeholder="默认不填写" />
        </el-form-item>

        <el-form-item label="授权代理人:">
          <el-input v-model="formData.authorizedAgent" placeholder="默认不填写" />
        </el-form-item>

        <el-form-item label="纳税识别号:" prop="taxId">
          <el-input v-model="formData.taxId" />
        </el-form-item>

        <el-form-item label="开户行地址:" prop="bankAddress">
          <el-input v-model="formData.bankAddress" />
        </el-form-item>

        <el-form-item label="银行账号:" prop="bankAccount">
          <el-input v-model="formData.bankAccount" />
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
  companyName: '',
  productTonnage: '',
  unitPrice: '',
  specialPrice: '',
  phoneNumber: '',
  companyAddress: '',
  legalRepresentative: '',
  authorizedAgent: '',
  taxId: '',
  bankAddress: '',
  bankAccount: ''
})

const formRef = ref(null)

const selectedCompanyId = ref(null) // 选中的公司ID

// 验证规则
const rules = reactive({
  contractNumber: [
    { required: true, message: '请输入合同编号', trigger: 'blur' },
    { pattern: /^\d+$/, message: '合同编号必须是数字', trigger: 'blur' }
  ],
  signingDate: [
    { required: true, message: '请输入签订日期', trigger: 'blur' },
  ],
  companyName: [
    { required: true, message: '请输入公司名称', trigger: 'blur' }
  ],
  productTonnage: [
    { required: true, message: '请输入商品吨位', trigger: 'blur' },
    { pattern: /^[0-9]+(\.[0-9]+)?$/, message: '商品吨位必须是数字(整数或小数)', trigger: 'blur' }
  ],
  unitPrice: [
    { required: true, message: '请输入商品单价', trigger: 'blur' },
    { pattern: /^[0-9]+$/, message: '商品单价必须是整数', trigger: 'blur' }
  ],
  taxId: [
    { required: true, message: '请输入纳税识别号', trigger: 'blur' }
  ],
  bankAddress: [
    { required: true, message: '请输入开户地址', trigger: 'blur' }
  ],
  bankAccount: [
    { required: true, message: '请输入银行账号', trigger: 'blur' }
  ]
})

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

// 用户选择了建议
const handleSelectCompany = (company) => {
  formData.companyName = company.name
  formData.phoneNumber = company.phone || ''
  formData.companyAddress = company.address || ''
  formData.legalRepresentative = company.legal_person || ''
  formData.authorizedAgent = company.agent || ''
  formData.taxId = company.tax_id || ''
  formData.bankAddress = company.bank_address || ''
  formData.bankAccount = company.bank_account || ''
  selectedCompanyId.value = company.id || null
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return;

  await formRef.value.validate(async (valid) => {
    if (!valid) {
      ElMessage.error('请完善必填信息后再提交！');
      return;
    }

    try {
      if (selectedCompanyId.value) {
        // 更新公司信息
        await updateCompany(selectedCompanyId.value, {
          name: formData.companyName,
          phone: formData.phoneNumber,
          address: formData.companyAddress,
          legal_person: formData.legalRepresentative,
          agent: formData.authorizedAgent,
          tax_id: formData.taxId,
          bank_address: formData.bankAddress,
          bank_account: formData.bankAccount
        })
      } else {
        // 新建公司
        await createCompany({
          name: formData.companyName,
          phone: formData.phoneNumber,
          address: formData.companyAddress,
          legal_person: formData.legalRepresentative,
          agent: formData.authorizedAgent,
          tax_id: formData.taxId,
          bank_address: formData.bankAddress,
          bank_account: formData.bankAccount
        })
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
  /* 设置最小高度为视口高度 */
  min-height: calc(var(--vh, 1vh) * 100);
  /* 移动端兼容 */
  width: 100%;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.form-card {
  width: 100%;
  max-width: 1200px;
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
  max-width: 800px;
  margin: 0 auto;
}

/* 让label和input在同一行 */
:deep(.el-form-item__content) {
  margin-left: 0 !important;
}

:deep(.el-form-item) {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

:deep(.el-form-item__label) {
  flex: 0 0 120px;
  text-align: right;
  font-weight: bold;
}

:deep(.el-form-item__content) {
  flex: 1;
}

.submit-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

.submit-button {
  width: 100%;
  max-width: 500px;
  font-size: 20px;
  height: 50px;
  padding: 10px 20px;
}

/* 响应式设计 */
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
    margin-bottom: 15px;
  }

  :deep(.el-form-item__label) {
    flex: 0 0 100px;
    padding-right: 10px;
    font-size: 14px;
  }

  .submit-button {
    font-size: 18px;
    height: 45px;
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
    margin-bottom: 10px;
  }

  :deep(.el-form-item__label) {
    flex: 0 0 90px;
    font-size: 13px;
  }

  .submit-button {
    font-size: 16px;
    height: 40px;
  }
}

/* 增加表单项的上下间距 */
:deep(.el-form-item) {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
  /* 增加底部间距，原来是 20px */
}

/* 增加输入框的高度和内部上下间距 */
:deep(.el-input__inner) {
  height: 45px;
  /* 增加输入框高度，默认是 32px */
  padding-top: 10px;
  padding-bottom: 10px;
  line-height: 25px;
}

/* 媒体查询中也要相应调整 */
@media (max-width: 768px) {
  :deep(.el-form-item) {
    flex-direction: row;
    margin-bottom: 25px;
    /* 中等屏幕的间距略小 */
  }

  :deep(.el-input__inner) {
    height: 40px;
    padding-top: 8px;
    padding-bottom: 8px;
  }
}

@media (max-width: 480px) {
  :deep(.el-form-item) {
    margin-bottom: 20px;
    /* 小屏幕再略小些 */
  }

  :deep(.el-input__inner) {
    height: 38px;
    padding-top: 7px;
    padding-bottom: 7px;
  }
}

/* 增加表单项的上下间距 */
:deep(.el-form-item) {
  display: flex;
  align-items: center;
  margin-bottom: 25px;
  /* 适当的表单项间距 */
}

/* 设置输入框高度为38px */
:deep(.el-input__inner) {
  height: 38px !important;
  /* 强制所有输入框高度为38px */
  line-height: 38px;
}

/* 响应式设计中保持输入框高度一致 */
@media (max-width: 768px) {
  :deep(.el-form-item) {
    flex-direction: row;
    margin-bottom: 20px;
  }

  :deep(.el-input__inner) {
    height: 38px !important;
    /* 中等屏幕保持相同高度 */
  }
}

@media (max-width: 480px) {
  :deep(.el-form-item) {
    margin-bottom: 15px;
  }

  :deep(.el-input__inner) {
    height: 38px !important;
    /* 小屏幕也保持相同高度 */
  }
}
</style>