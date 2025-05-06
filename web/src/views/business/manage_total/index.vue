<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives, watch } from 'vue'
import { NButton, NForm, NFormItem, NInput, NPopconfirm, NInputNumber, NSwitch, NSelect } from 'naive-ui'
import * as XLSX from 'xlsx'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

import { renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'

defineOptions({ name: 'YY网页' })

const $table = ref(null)
const queryItems = ref({})

// 获取权限指令（如果有）
const vPermission = resolveDirective('permission')

// 使用 useCRUD 封装总表数据的增删改查，新增字段：内勤、平台、支出
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
    date: null,
    plate: '',
    region: '',
    company: '',
    field_staff: '',      // 外勤
    internal_staff: '',   // 内勤
    expected_expenditure: 0,
    income: 0,
    destination: '',
    remark: '',
    docking_time: null,
    handover_time: null,
    is_completed: false,
  },
  doCreate: api.createTotal,
  doUpdate: api.updateTotal,
  doDelete: api.deleteTotal,
  refresh: () => $table.value?.handleSearch(),
})

const internalStaffOptions = ref([])
const fieldStaffOptions = ref([])
const businessUserOptions = ref([])

const fetchDutyStaffOptions = async (type) => {
  const response = await api.getDutyStaffList({ type })
  return response.data.map(staff => ({ label: staff.name, value: staff.name }))
}

const fetchBusinessUserOptions = async () => {
  const response = await api.getUserList({ dept_id: 5 })
  return response.data.map(user => ({ label: user.username, value: user.username }))
}

onMounted(async () => {
  internalStaffOptions.value = await fetchDutyStaffOptions('内勤人员')
  fieldStaffOptions.value = await fetchDutyStaffOptions('外勤人员')
  businessUserOptions.value = await fetchBusinessUserOptions()
  $table.value?.handleSearch()
})

// XLSX 导出方法，导出时包含所有字段
const exportToExcel = async () => {
  try {
    const queryParams = { ...queryItems.value, page: 1, page_size: 99999 }
    const response = await api.getTotalList(queryParams)
    if (!response || !response.data || response.data.length === 0) {
      window.$message?.warning('无数据可导出')
      return
    }
    const data = response.data.map(row => ({
      '日期': row.date,
      '车牌': row.plate,
      '区域': row.region,
      '公司': row.company,
      '外勤': row.field_staff,
      '内勤': row.internal_staff,
      '预期支出': row.expected_expenditure,
      '收入': row.income,
      '去向': row.destination,
      '备注': row.remark,
      '对接时间': row.docking_time,
      '交接时间': row.handover_time,
      '是否完成': row.is_completed ? '是' : '否',
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
  $table.value?.handleSearch()
}

// 表单验证规则，新增内勤、平台、支出字段规则
const addAPIRules = {
  date: [
    { required: true, message: '请输入日期', trigger: ['input', 'blur', 'change'] },
  ],
  plate: [
    { required: true, message: '请输入车牌', trigger: ['input', 'blur', 'change'] },
  ],
  region: [
    { required: true, message: '请输入区域', trigger: ['input', 'blur', 'change'] },
  ],
  company: [
    { required: true, message: '请输入公司', trigger: ['input', 'blur', 'change'] },
  ],
  field_staff: [
    { required: true, message: '请选择外勤人员', trigger: ['input', 'blur', 'change'] },
  ],
  internal_staff: [
    { required: true, message: '请选择内勤人员', trigger: ['input', 'blur', 'change'] },
  ],
  expected_expenditure: [
    { required: true, message: '请输入预期支出', trigger: ['input', 'blur', 'change'], type: 'number' },
  ],
  income: [
    { required: true, message: '请输入收入', trigger: ['input', 'blur', 'change'], type: 'number' },
  ],
  destination: [
    { required: false, message: '请输入去向', trigger: ['input', 'blur', 'change'] },
  ],
  docking_time: [
    { required: false, message: '请输入对接时间', trigger: ['input', 'blur', 'change'] },
  ],
  handover_time: [
    { required: false, message: '请输入交接时间', trigger: ['input', 'blur', 'change'] },
  ],
}

// 表格列配置，增加内勤、平台、支出列
const columns = [
  { title: '日期', key: 'date', width: 110, align: 'center', ellipsis: { tooltip: true } },
  { title: '车牌', key: 'plate', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '区域', key: 'region', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '公司', key: 'company', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '外勤', key: 'field_staff', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '内勤', key: 'internal_staff', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '预期支出', key: 'expected_expenditure', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '收入', key: 'income', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '去向', key: 'destination', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '备注', key: 'remark', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '对接时间', key: 'docking_time', width: 180, align: 'center', ellipsis: { tooltip: true } },
  { title: '交接时间', key: 'handover_time', width: 180, align: 'center', ellipsis: { tooltip: true } },
  {
    title: '是否完成', key: 'is_completed', width: 'auto', align: 'center',
    render(row) { return row.is_completed ? '是' : '否' }
  },
  {
    title: '操作',
    key: 'actions',
    width: 'auto',
    align: 'center',
    fixed: 'right',
    render(row) {
      return [
        withDirectives(
          h(
            NButton,
            {
              size: 'small',
              type: 'primary',
              style: 'margin-right: 8px;',
              onClick: () => { handleEdit(row) },
            },
            { default: () => '编辑', icon: renderIcon('material-symbols:edit', { size: 16 }) }
          ),
          [[vPermission, 'post/api/v1/total/update']]
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ id: row.id }, false),
            onNegativeClick: () => { },
          },
          {
            trigger: () =>
              withDirectives(
                h(
                  NButton,
                  { size: 'small', type: 'error', style: 'margin-right: 8px;' },
                  { default: () => '删除', icon: renderIcon('material-symbols:delete-outline', { size: 16 }) }
                ),
                [[vPermission, 'delete/api/v1/total/delete']]
              ),
            default: () => h('div', {}, '确定删除该记录吗?'),
          }
        ),
      ]
    },
  },
]
</script>

<template>
  <CommonPage show-footer title="数据展示">
    <template #action>
      <div>
        <NButton v-permission="'post/api/v1/total/refresh'" class="float-right mr-15" type="warning"
          @click="handleRefreshApi">
          <TheIcon icon="material-symbols:refresh" :size="18" class="mr-5" />刷新记录
        </NButton>
        <NButton type="success" class="float-right mr-15" @click="exportToExcel">
          <TheIcon icon="material-symbols:download" :size="18" class="mr-5" />
          导出Excel
        </NButton>
      </div>
    </template>
    <!-- 表格展示 -->
    <CrudTable ref="$table" v-model:query-items="queryItems" :columns="columns" :get-data="api.getTotalList">
      <template #queryBar>
        <QueryBarItem label="日期" :label-width="40">
          <n-date-picker v-model:formatted-value="queryItems.date" type="date" clearable placeholder="请选择日期"
            @update="$table?.handleSearch()" />
        </QueryBarItem>
        <QueryBarItem label="车牌" :label-width="40">
          <NInput v-model:value="queryItems.plate" clearable placeholder="请输入车牌"
            @keypress.enter="$table?.handleSearch()" />
        </QueryBarItem>
        <QueryBarItem label="业务" :label-width="40">
          <NInput v-model:value="queryItems.business" clearable placeholder="请输入业务名称"
            @keypress.enter="$table?.handleSearch()" />
        </QueryBarItem>
        <QueryBarItem label="公司" :label-width="40">
          <NInput v-model:value="queryItems.company" clearable placeholder="请输入公司名称"
            @keypress.enter="$table?.handleSearch()" />
        </QueryBarItem>
      </template>
    </CrudTable>

    <!-- 新增/编辑 弹窗 -->
    <CrudModal v-model:visible="modalVisible" :title="modalTitle" :loading="modalLoading" @save="handleSave">
      <NForm ref="modalFormRef" label-placement="left" label-align="left" :label-width="80" :model="modalForm"
        :rules="addAPIRules">
        <NFormItem label="日期" path="date">
          <n-date-picker v-model:formatted-value="modalForm.date" type="date" clearable value-format="yyyy-MM-dd" />
        </NFormItem>
        <NFormItem label="车牌" path="plate">
          <NInput v-model:value="modalForm.plate" clearable placeholder="请输入车牌" />
        </NFormItem>
        <NFormItem label="区域" path="region">
          <NInput v-model:value="modalForm.region" clearable placeholder="请输入区域" />
        </NFormItem>
        <NFormItem label="公司" path="company">
          <NInput v-model:value="modalForm.company" clearable placeholder="请输入公司" />
        </NFormItem>
        <NFormItem label="外勤" path="field_staff">
          <NSelect v-model:value="modalForm.field_staff" clearable placeholder="请选择外勤人员" :options="fieldStaffOptions"
            filterable />
        </NFormItem>
        <NFormItem label="内勤" path="internal_staff">
          <NSelect v-model:value="modalForm.internal_staff" clearable placeholder="请选择内勤人员"
            :options="internalStaffOptions" filterable />
        </NFormItem>
        <NFormItem label="预期支出" path="expected_expenditure">
          <NInputNumber v-model:value="modalForm.expected_expenditure" placeholder="请输入预期支出">
            <template #prefix>
              ￥
            </template>
          </NInputNumber>
        </NFormItem>
        <NFormItem label="收入" path="income">
          <NInputNumber v-model:value="modalForm.income" placeholder="请输入收入">
            <template #prefix>
              ￥
            </template>
          </NInputNumber>
        </NFormItem>
        <NFormItem label="去向" path="destination">
          <NInput v-model:value="modalForm.destination" clearable placeholder="请输入去向" />
        </NFormItem>
        <NFormItem label="备注" path="remark">
          <NInput v-model:value="modalForm.remark" clearable placeholder="请输入备注" />
        </NFormItem>
        <NFormItem label="对接时间" path="docking_time">
          <n-date-picker v-model:formatted-value="modalForm.docking_time" type="datetime" clearable
            value-format="yyyy-MM-dd HH:mm:ss" />
        </NFormItem>
        <NFormItem label="交接时间" path="handover_time">
          <n-date-picker v-model:formatted-value="modalForm.handover_time" type="datetime" clearable
            value-format="yyyy-MM-dd HH:mm:ss" />
        </NFormItem>
        <NFormItem label="是否完成" path="is_completed">
          <NSwitch v-model:value="modalForm.is_completed" :checked-value="true" :unchecked-value="false" />
        </NFormItem>
      </NForm>
    </CrudModal>
  </CommonPage>
</template>
