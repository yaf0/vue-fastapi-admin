<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
import { NButton, NForm, NFormItem, NInput, NPopconfirm, NSelect } from 'naive-ui'
import * as XLSX from 'xlsx'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

import { renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'

defineOptions({ name: '勤务人员管理' })

const $table = ref(null)
const queryItems = ref({
  name: '',
  type: '',
})

// 获取权限指令（如果有）
const vPermission = resolveDirective('permission')

// 使用 useCRUD 封装勤务人员数据的增删改查
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
  name: '勤务人员',
  initForm: {
    name: '',                          // 人员名称
    type: "外勤人员",  // 人员类型
  },
  doCreate: api.createDutyStaff,
  doUpdate: api.updateDutyStaff,
  doDelete: api.deleteDutyStaff,
  refresh: () => $table.value?.handleSearch(),
})

onMounted(() => {
  $table.value?.handleSearch()
})

// XLSX 导出方法，导出时包含所有字段
const exportToExcel = async () => {
  try {
    const queryParams = { ...queryItems.value, page: 1, per_page: 99999 }
    const response = await api.getDutyStaffList(queryParams)
    if (!response || !response.data || response.data.length === 0) {
      window.$message?.warning('无数据可导出')
      return
    }
    const data = response.data.map(row => ({
      '人员名称': row.name,
      '人员类型': row.type,
      '创建时间': row.created_at.split('T')[0],  // 格式化日期为 yyyy-MM-dd
    }))
    const ws = XLSX.utils.json_to_sheet(data)
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, '勤务人员数据')
    XLSX.writeFile(wb, `勤务人员数据_${new Date().toISOString().slice(0, 10)}.xlsx`)
  } catch (error) {
    console.error('导出 Excel 失败:', error)
    window.$message?.error('导出失败，请检查网络或稍后重试')
  }
}

// 表单验证规则
const addAPIRules = {
  name: [
    { required: true, message: '请输入人员名称', trigger: ['input', 'blur', 'change'] },
  ],
  type: [
    { required: true, message: '请选择人员类型', trigger: ['input', 'blur', 'change'] },
  ],
}

// 表格列配置
const columns = [
  { title: '人员名称', key: 'name', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '人员类型', key: 'type', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '创建时间', key: 'created_at', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
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
          [[vPermission, 'post/api/v1/duty_staff/update']]
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
                [[vPermission, 'delete/api/v1/duty_staff/delete']]
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
  <CommonPage show-footer title="勤务人员管理">
    <template #action>
      <div>
        <NButton v-permission="'post/api/v1/duty_staff/create'" class="float-right mr-15" type="primary"
          @click="handleAdd">
          <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />新建勤务人员
        </NButton>
        <NButton type="success" class="float-right mr-15" @click="exportToExcel">
          <TheIcon icon="material-symbols:download" :size="18" class="mr-5" />
          导出Excel
        </NButton>
      </div>
    </template>

    <!-- 表格展示 -->
    <CrudTable ref="$table" v-model:query-items="queryItems" :columns="columns" :get-data="api.getDutyStaffList">
      <template #queryBar>
        <QueryBarItem label="人员名称" :label-width="70">
          <NInput v-model:value="queryItems.name" clearable placeholder="请输入人员名称"
            @keypress.enter="$table?.handleSearch()" />
        </QueryBarItem>
        <QueryBarItem label="人员类型" :label-width="70">
          <NSelect v-model:value="queryItems.type" placeholder="请选择人员类型" :options="[
            { label: '内勤人员', value: '内勤人员' },
            { label: '外勤人员', value: '外勤人员' },
          ]" @update:value="$table?.handleSearch()" style="width: 200px;" />
        </QueryBarItem>
      </template>
    </CrudTable>

    <!-- 新增/编辑 弹窗 -->
    <CrudModal v-model:visible="modalVisible" :title="modalTitle" :loading="modalLoading" @save="handleSave">
      <NForm ref="modalFormRef" :model="modalForm" :rules="addAPIRules">
        <NFormItem label="人员名称" path="name">
          <NInput v-model:value="modalForm.name" clearable placeholder="请输入人员名称" />
        </NFormItem>
        <NFormItem label="人员类型" path="type">
          <NSelect v-model:value="modalForm.type" clearable placeholder="请选择人员类型" :options="[
            { label: '内勤人员', value: '内勤人员' },
            { label: '外勤人员', value: '外勤人员' },
          ]" />
        </NFormItem>
      </NForm>
    </CrudModal>
  </CommonPage>
</template>