<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives, watch } from 'vue'
import { NButton, NForm, NFormItem, NInput, NPopconfirm, NInputNumber, NSwitch, NSelect, NStatistic} from 'naive-ui'
import * as XLSX from 'xlsx'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

import { renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'
import { onClickOutside } from '@vueuse/core'
import { value } from 'lodash-es'

defineOptions({ name: '业务员数据展示' })

const $table = ref(null)
const queryItems = ref({})
const statistics = ref({
  count: 0,
  expected_expenditure_sum: 0,
  income_sum: 0,
  profit_sum: 0,
})

// 获取权限指令（如果有）
const vPermission = resolveDirective('permission')

// 使用 useCRUD 封装总表数据的增删改查，新增字段：外勤、预期支出、实际支出
const {
  modalVisible,
  modalTitle,
  modalLoading,
  handleSave,
  modalForm,
  modalFormRef,
  handleEdit,
  handleDelete,
  handleAdd,
} = useCRUD({
  name: '总表数据',
  // 初始化表单数据，字段与后端保持一致
  initForm: {
    business: '',
    count: 0,
    expected_expenditure: 0,
    income: 0,
    profit: 0,
  },
  refresh: async () => {
    const response = await api.getTotalListBs(queryItems.value)
    if (response) {
      statistics.value.count = response.count
      statistics.value.expected_expenditure_sum = response.expected_expenditure_sum
      statistics.value.income_sum = response.income_sum
    }
    $table.value?.handleSearch()
  },
})

const businessUserOptions = ref([])

const fetchBusinessUserOptions = async () => {
  const response = await api.getUserList({ dept_id: 5 })
  return response.data.map(user => ({ label: user.username, value: user.username }))
}

onMounted(async () => {
  businessUserOptions.value = await fetchBusinessUserOptions()
  // $table.value?.handleSearch()
  handleRefreshApi()
})

// XLSX 导出方法，导出时包含所有字段
const exportToExcel = async () => {
  try {
    const queryParams = { ...queryItems.value, page: 1, per_page: 99999 }
    const response = await api.getTotalListBs(queryParams)
    if (!response || !response.data || response.data.length === 0) {
      window.$message?.warning('无数据可导出')
      return
    }
    const data = response.data.map(row => ({
      '业务': row.business,
      '台数': row.count,
      '预期支出': row.expected_expenditure,
      '收入': row.income,
      '利润': row.income - row.expected_expenditure,
    }))
    const ws = XLSX.utils.json_to_sheet(data)
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, '业务维度统计')
    XLSX.writeFile(wb, `业务维度统计_${new Date().toISOString().slice(0, 10)}.xlsx`)
  } catch (error) {
    console.error('导出 Excel 失败:', error)
    window.$message?.error('导出失败，请检查网络或稍后重试')
  }
}

async function handleRefreshApi() {
  const response = await api.getTotalListBs(queryItems.value)
  if (response) {
    statistics.value.count_sum = response.count_sum
    statistics.value.expected_expenditure_sum = response.expected_expenditure_sum
    statistics.value.income_sum = response.income_sum
  }
  $table.value?.handleSearch()
}

// 表格列配置，增加外勤、预期支出、实际支出列
const columns = [
  {
    title: '业务',
    key: 'business',
    align: 'center',
  },
  {
    title: '台数',
    key: 'count',
    align: 'center',
  },
  {
    title: '预期支出',
    key: 'expected_expenditure',
    align: 'center',
  },
  {
    title: '收入',
    key: 'income',
    align: 'center',
  },
  {
    title: '利润',
    key: 'profit',
    align: 'center',
    render(row) {
      return row.income - row.expected_expenditure
    },
  },
]
</script>

<template>
  <CommonPage show-footer title="业务维度数据">
    <div flex flex-wrap>
      <n-card
        class="mb-10 mt-10 w-200"
        hover:card-shadow
        title="业务"
        size="small"
      >
        <p op-60>{{ queryItems.business || '所有' }} </p>
      </n-card>
      <n-card
        class="mb-10 mt-10 w-200"
        hover:card-shadow
        title="台数"
        size="small"
      >
        <p op-60>{{ statistics.count_sum }}</p> 
      </n-card>
      <n-card
        class="mb-10 mt-10 w-200"
        hover:card-shadow
        title="应支出总计"
        size="small"
      >
        <p op-60>{{ statistics.expected_expenditure_sum }}</p> 
      </n-card>
      <n-card
        class="mb-10 mt-10 w-200"
        hover:card-shadow
        title="收入总计"
        size="small"
      >
        <p op-60>{{ statistics.income_sum }}</p> 
      </n-card>
      <n-card
        class="mb-10 mt-10 w-200"
        hover:card-shadow
        title="利润总计"
        size="small"
      >
        <p op-60>{{ statistics.income_sum - statistics.expected_expenditure_sum }}</p>
      </n-card>
    </div>
    <template #action>
      <div>
        <NButton type="success" class="float-right mr-15" @click="exportToExcel">
          <TheIcon icon="material-symbols:download" :size="18" class="mr-5" />
          导出Excel
        </NButton>
      </div>
    </template>
    <!-- 表格展示 -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getTotalListBs"
      @update:query-items="handleRefreshApi"
    >
      <template #queryBar>
        <QueryBarItem label="业务" :label-width="70">
          <NSelect
            v-model:value="queryItems.business"
            clearable
            placeholder="输入或选择业务"
            :options="businessUserOptions"
            filterable
            @update:value="handleRefreshApi"
            
          />
        </QueryBarItem>
      </template>
    </CrudTable>
  </CommonPage>
</template>

