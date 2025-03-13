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

defineOptions({ name: 'YY外勤' })

const $table = ref(null)
const queryItems = ref({})
const statistics = ref({
  total_count: 0,
  total_expected_expenditure_sum: 0,
  total_actual_expenditure: 0,
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
    plate: '',
    business: '',
    field_staff: '',      // 外勤
    expected_expenditure: 0,
    actual_expenditure: 0,
  },
  refresh: async () => {
    const response = await api.getDutyStaffListfs(queryItems.value)
    if (response) {
      statistics.value.total_count = response.total_count
      statistics.value.total_expected_expenditure_sum = response.total_expected_expenditure_sum
      statistics.value.total_actual_expenditure = response.total_actual_expenditure
    }
    $table.value?.handleSearch()
  },
})

const fieldStaffOptions = ref([])

const fetchDutyStaffOptions = async (type) => {
  const response = await api.getDutyStaffList({ type })
  return response.data.map(staff => ({ label: staff.name, value: staff.name }))
}

onMounted(async () => {
  fieldStaffOptions.value = await fetchDutyStaffOptions('外勤人员')
  handleRefreshApi()
})

// XLSX 导出方法，导出时包含所有字段
const exportToExcel = async () => {
  try {
    const queryParams = { ...queryItems.value, page: 1, per_page: 99999 }
    const response = await api.getDutyStaffListfs(queryParams)
    if (!response || !response.data || response.data.length === 0) {
      window.$message?.warning('无数据可导出')
      return
    }
    const data = response.data.map(row => ({
      '外勤': row.name,
      '台数': row.count,
      '预期支出总计': row.expected_expenditure_sum,
      '实际支出': row.actual_expenditure,
    }))
    const ws = XLSX.utils.json_to_sheet(data)
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, '总表数据')
    XLSX.writeFile(wb, `总表数据_${new Date().toISOString().slice(0, 10)}.xlsx`)
  } catch (error) {
    console.error('导出 Excel 失败:', error)
    window.$message?.error('导出失败，请检查网络或稍后重试')
  }
}

async function handleRefreshApi() {
  const response = await api.getDutyStaffListfs(queryItems.value)
  if (response) {
    statistics.value.total_count = response.total_count
    statistics.value.total_expected_expenditure_sum = response.total_expected_expenditure_sum
    statistics.value.total_actual_expenditure = response.total_actual_expenditure
  }
  $table.value?.handleSearch()
}

const handleUpdateExpenditure = async (value, row) => {
  if (isNaN(value) || value === '' || value === null || value === undefined) {
    window.$message?.warning('实际支出必须是数字且不能为空')
    return
  }
  row.actual_expenditure = value
  await api.updateDutyStaff({
    id: row.id,
    name: row.name,
    type: row.type,
    actual_expenditure: value
  })
  window.$message?.success('实际支出更新成功')
}

// 表格列配置，增加外勤、预期支出、实际支出列
const columns = [
  { title: '外勤', key: 'name', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '台数', key: 'count', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '预期支出', key: 'expected_expenditure_sum', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '实际支出', key: 'actual_expenditure', width: 'auto', align: 'center', ellipsis: { tooltip: true },

    render(row) {
      return h(NInputNumber, {
        value: row.actual_expenditure,
        onUpdateValue: (value) => {
          handleUpdateExpenditure(value, row)
        },
        placeholder: '请输入实际支出',
      })
    }
  },
  { title: '差额', key: 'difference', width: 'auto', align: 'center', ellipsis: { tooltip: true },
    render(row) {
      return row.expected_expenditure_sum - row.actual_expenditure
    }
  },
]
</script>

<template>
  <CommonPage show-footer title="外勤数据展示">
    <div flex flex-wrap>
      <n-card
        class="mb-10 mt-10 w-300"
        hover:card-shadow
        title="外勤人员"
        size="small"
      >
        <p op-60>{{ queryItems.field_staff || '所有' }} </p>
      </n-card>
      <n-card
        class="mb-10 mt-10 w-300"
        hover:card-shadow
        title="台数"
        size="small"
      >
        <p op-60>{{ statistics.total_count }}</p> 
      </n-card>
      <n-card
        class="mb-10 mt-10 w-300"
        hover:card-shadow
        title="应支出总计"
        size="small"
      >
        <p op-60>{{ statistics.total_expected_expenditure_sum }}</p> 
      </n-card>
      <n-card
        class="mb-10 mt-10 w-300"
        hover:card-shadow
        title="实际支出总计"
        size="small"
      >
        <p op-60>{{ statistics.total_actual_expenditure }}</p> 
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
      :get-data="api.getDutyStaffListfs"
      @update:query-items="handleRefreshApi"
    >
      <template #queryBar>
        <QueryBarItem label="外勤人员" :label-width="70">
          <NSelect
            v-model:value="queryItems.field_staff"
            clearable
            placeholder="输入或选择外勤人员"
            :options="fieldStaffOptions"
            filterable
            @update:value="handleRefreshApi"
            
          />
        </QueryBarItem>
      </template>
    </CrudTable>
  </CommonPage>
</template>

