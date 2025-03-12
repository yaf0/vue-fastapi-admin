<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives, watch } from 'vue'
import { NButton, NForm, NFormItem, NInput, NPopconfirm, NInputNumber, NSwitch, NSelect, NStatistic } from 'naive-ui'
import * as XLSX from 'xlsx'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

import { renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'

defineOptions({ name: 'YY外勤' })

const $table = ref(null)
const queryItems = ref({})
const statistics = ref({
  count: 0,
  expected_expenditure_sum: 0,
  actual_expenditure_sum: 0,
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
  doUpdate: api.updateTotalYyfs,
  refresh: () => $table.value?.handleSearch(),
})

const fieldStaffOptions = ref([])

const fetchDutyStaffOptions = async (type) => {
  const response = await api.getDutyStaffList({ type })
  return response.data.map(staff => ({ label: staff.name, value: staff.name }))
}

onMounted(async () => {
  fieldStaffOptions.value = await fetchDutyStaffOptions('外勤人员')
  $table.value?.handleSearch()
})

// XLSX 导出方法，导出时包含所有字段
const exportToExcel = async () => {
  try {
    const queryParams = { ...queryItems.value, page: 1, per_page: 99999 }
    const response = await api.getTotalListYyfs(queryParams)
    if (!response || !response.data || response.data.length === 0) {
      window.$message?.warning('无数据可导出')
      return
    }
    const data = response.data.map(row => ({
      '车牌': row.plate,
      '业务': row.business,
      '外勤': row.field_staff,
      '预期支出': row.expected_expenditure,
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
  const response = await $table.value?.handleSearch()
  if (response && response.extra) {
    statistics.value.count = response.extra.count
    statistics.value.expected_expenditure_sum = response.extra.expected_expenditure_sum
    statistics.value.actual_expenditure_sum = response.extra.actual_expenditure_sum
  }
}

// 表格列配置，增加外勤、预期支出、实际支出列
const columns = [
  { title: '车牌', key: 'plate', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '业务', key: 'business', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '外勤', key: 'field_staff', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '预期支出', key: 'expected_expenditure', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { 
    title: '实际支出', key: 'actual_expenditure', width: 'auto', align: 'center', ellipsis: { tooltip: true },
    render(row) {
      return h(NInputNumber, {
        value: row.actual_expenditure,
        onUpdateValue: async (value) => {
          row.actual_expenditure = value
          await api.updateTotalYyfs({ id: row.id, actual_expenditure: value })
          window.$message?.success('实际支出更新成功')
        },
        placeholder: '请输入实际支出',
      })
    }
  },
]
</script>

<template>
  <CommonPage show-footer title="外勤数据展示">
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
      :get-data="api.getTotalListYyfs"
      @update:query-items="handleRefreshApi"
    >
      <template #queryBar>
        <QueryBarItem label="外勤人员" :label-width="70">
          <NSelect
            v-model:value="queryItems.field_staff"
            clearable
            placeholder="请选择外勤人员"
            :options="fieldStaffOptions"
            filterable
            @update="$table?.handleSearch()"
          />
        </QueryBarItem>
      </template>
    </CrudTable>
    <!-- 统计数据展示 -->
    <div class="statistics">
      <NStatistic label="台数" :value="statistics.count" />
      <NStatistic label="预期支出总计" :value="statistics.expected_expenditure_sum" />
      <NStatistic label="实际支出总计" :value="statistics.actual_expenditure_sum" />
    </div>
  </CommonPage>
</template>

