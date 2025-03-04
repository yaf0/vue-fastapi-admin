<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
import { NButton, NForm, NFormItem, NInput, NPopconfirm, NInputNumber, NSwitch } from 'naive-ui'
import * as XLSX from 'xlsx'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

import { renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'

defineOptions({ name: '外勤记录数据管理' })

const $table = ref(null)
const queryItems = ref({})

// 获取权限指令（如果有）
const vPermission = resolveDirective('permission')

// 使用 useCRUD 封装外勤记录数据的增删改查
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
  name: '外勤记录数据',
  initForm: {
    name: '',                          // 外勤名称
    number: 0,                          // 台数
    expected_expenditure: 0,            // 预期支出
    actual_expenditure: 0,              // 实际支出
    difference: 0,                      // 差额
    date: null,                         // 日期
    remark: '',                         // 备注
  },
  doCreate: api.createFieldWork,
  doUpdate: api.updateFieldWork,
  doDelete: api.deleteFieldWork,
  refresh: () => $table.value?.handleSearch(),
})

onMounted(() => {
  $table.value?.handleSearch()
})

// XLSX 导出方法，导出时包含所有字段
const exportToExcel = async () => {
  try {
    const queryParams = { ...queryItems.value, page: 1, per_page: 99999 }
    const response = await api.getFieldWorkList(queryParams)
    if (!response || !response.data || response.data.length === 0) {
      window.$message?.warning('无数据可导出')
      return
    }
    const data = response.data.map(row => ({
      '外勤名称': row.name,
      '台数': row.number,
      '预期支出': row.expected_expenditure,
      '实际支出': row.actual_expenditure,
      '差额': row.difference,
      '日期': row.date.split('T')[0],  // 格式化日期为 yyyy-MM-dd
      '备注': row.remark,
    }))
    const ws = XLSX.utils.json_to_sheet(data)
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, '外勤数据')
    XLSX.writeFile(wb, `外勤数据_${new Date().toISOString().slice(0, 10)}.xlsx`)
  } catch (error) {
    console.error('导出 Excel 失败:', error)
    window.$message?.error('导出失败，请检查网络或稍后重试')
  }
}

async function handleRefreshApi() {
  $table.value?.handleSearch()
}

// 表单验证规则，新增字段：外勤名称、台数、支出、差额等
const addAPIRules = {
  name: [
    { required: true, message: '请输入外勤名称', trigger: ['input', 'blur', 'change'] },
  ],
  number: [
    { required: true, message: '请输入台数', trigger: ['input', 'blur', 'change'], type: 'number' },
  ],
  expected_expenditure: [
    { required: true, message: '请输入预期支出', trigger: ['input', 'blur', 'change'], type: 'number' },
  ],
  actual_expenditure: [
    { required: true, message: '请输入实际支出', trigger: ['input', 'blur', 'change'], type: 'number' },
  ],
  difference: [
    { required: true, message: '请输入差额', trigger: ['input', 'blur', 'change'], type: 'number' },
  ],
  date: [
    { required: true, message: '请选择日期', trigger: ['input', 'blur', 'change'] },
  ],
  remark: [
    { required: false, message: '请输入备注', trigger: ['input', 'blur', 'change'] },
  ],
}

// 表格列配置，增加字段：外勤名称、台数、支出、差额等
const columns = [
  { title: '外勤名称', key: 'name', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '台数', key: 'number', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '预期支出', key: 'expected_expenditure', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '实际支出', key: 'actual_expenditure', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '差额', key: 'difference', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '日期', key: 'date', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '备注', key: 'remark', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
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
          [[vPermission, 'put/api/v1/field-work/update']]
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ id: row.id }, false),
            onNegativeClick: () => {},
          },
          {
            trigger: () =>
              withDirectives(
                h(
                  NButton,
                  { size: 'small', type: 'error', style: 'margin-right: 8px;' },
                  { default: () => '删除', icon: renderIcon('material-symbols:delete-outline', { size: 16 }) }
                ),
                [[vPermission, 'delete/api/v1/field-work/delete']]
              ),
            default: () => h('div', {}, '确定删除该记录吗?'),
          }
        ),
      ]
    },
  },
]
// 监听预期支出和实际支出的变化，计算差额
watch(
  () => modalForm.value.expected_expenditure,
  () => {
    modalForm.value.difference = modalForm.value.expected_expenditure - modalForm.value.actual_expenditure
  }
)

watch(
  () => modalForm.value.actual_expenditure,
  () => {
    modalForm.value.difference = modalForm.value.expected_expenditure - modalForm.value.actual_expenditure
  }
)
</script>

<template>
  <CommonPage show-footer title="外勤数据管理">
    <div flex flex-wrap >
      <n-card
        class="mb-10 mt-10 w-300"
        hover:card-shadow
        title="台数"
        size="small"
      >
        <p op-60>123</p> 
      </n-card>
      <n-card
        class="mb-10 mt-10 w-300"
        hover:card-shadow
        title="应支出总计"
        size="small"
      >
        <p op-60>123</p> 
      </n-card>
      <n-card
        class="mb-10 mt-10 w-300"
        hover:card-shadow
        title="实际支出总计"
        size="small"
      >
        <p op-60>123</p> 
      </n-card>
    </div>
   
    <template #action>
      <div>
        <NButton
          v-permission="'post/api/v1/field-work/create'"
          class="float-right mr-15"
          type="primary"
          @click="handleAdd"
        >
          <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />新建外勤记录
        </NButton>
        <NButton
          v-permission="'post/api/v1/field-work/refresh'"
          class="float-right mr-15"
          type="warning"
          @click="handleRefreshApi"
        >
          <TheIcon icon="material-symbols:refresh" :size="18" class="mr-5" />刷新记录
        </NButton>
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
      :get-data="api.getFieldWorkList"
    >
      <template #queryBar>
        <QueryBarItem label="外勤名称" :label-width="70">
          <NInput
            v-model:value="queryItems.name"
            clearable
            placeholder="请输入外勤名称"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="日期" :label-width="70">
          <n-date-picker
            v-model:formatted-value="queryItems.date"
            type="date"
            clearable
            placeholder="请选择日期"
            @update="$table?.handleSearch()"
          />
        </QueryBarItem>
      </template>
    </CrudTable>

    <!-- 新增/编辑 弹窗 -->
    <CrudModal
      v-model:visible="modalVisible"
      :title="modalTitle"
      :loading="modalLoading"
      @save="handleSave"
    >
      <NForm ref="modalFormRef" :model="modalForm" :rules="addAPIRules">
        <NFormItem label="外勤名称" path="name">
          <NInput v-model:value="modalForm.name" clearable placeholder="请输入外勤名称" />
        </NFormItem>
        <NFormItem label="台数" path="number">
          <NInputNumber v-model:value="modalForm.number" placeholder="请输入台数" />
        </NFormItem>
        <NFormItem label="预期支出" path="expected_expenditure">
          <NInputNumber v-model:value="modalForm.expected_expenditure" placeholder="请输入预期支出" />
        </NFormItem>
        <NFormItem label="实际支出" path="actual_expenditure">
          <NInputNumber v-model:value="modalForm.actual_expenditure" placeholder="请输入实际支出" />
        </NFormItem>
        <NFormItem label="差额" path="difference">
          <NInputNumber v-model:value="modalForm.difference" :disabled="true" placeholder="自动计算差额" />
        </NFormItem>
        <NFormItem label="日期" path="date">
          <n-date-picker v-model:formatted-value="modalForm.date" type="date" clearable value-format="yyyy-MM-dd"/>
        </NFormItem>
        <NFormItem label="备注" path="remark">
          <NInput v-model:value="modalForm.remark" clearable placeholder="请输入备注" />
        </NFormItem>
      </NForm>
    </CrudModal>
  </CommonPage>
</template>

