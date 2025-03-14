<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
import { NButton, NForm, NFormItem, NInput, NPopconfirm, NSwitch, NSelect, NCheckbox } from 'naive-ui'
import * as XLSX from 'xlsx'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'
import { watch } from 'vue'

import { renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
import api from '@/api'
import { useUserStore } from '@/store'


defineOptions({ name: '我的记录' })

const $table = ref(null)
const queryItems = ref({})
const userStore = useUserStore()

// 获取权限指令（如果有）
const vPermission = resolveDirective('permission')

// 使用 useCRUD 封装总表数据的增删改查
const {
  modalVisible,
  modalTitle,
  modalLoading,
  handleSave,
  modalForm,
  modalFormRef,
  handleEdit,
} = useCRUD({
  name: '总表数据',
  // 初始化表单数据，字段与后端保持一致
  initForm: {
    remark: '',
  },
  doUpdate: api.updateTotalOb,
  refresh: () => $table.value?.handleSearch(),
})

onMounted(async () => {
  queryItems.value.business = userStore.name
  $table.value?.handleSearch()
})

watch(
  () => queryItems.value, // 监听 queryItems 变化
  () => {
    queryItems.value.business = userStore.name; // 每次变化时确保 business 更新
  },
  { immediate: true } // 立即执行一次，确保页面初始化时就有 business 参数
)

// XLSX 导出方法，导出时包含所有字段
const exportToExcel = async () => {
  try {
    queryItems.value.business = userStore.name
    const queryParams = { ...queryItems.value, business: userStore.name, page: 1, per_page: 99999 }
    const response = await api.getTotalListOb(queryParams)
    if (!response || !response.data || response.data.length === 0) {
      window.$message?.warning('无数据可导出')
      return
    }
    const data = response.data.map(row => ({
      '日期': row.date,
      '车牌': row.plate,
      '区域': row.region,
      '公司': row.company,
      '业务': row.business,
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
  queryItems.value.business = userStore.name
  $table.value?.handleSearch()
}

// 表单验证规则
const addAPIRules = {
  remark: [
    { required: false, message: '请输入备注', trigger: ['input', 'blur', 'change'] },
  ],
}

// 表格列配置
const columns = [
  { title: '日期', key: 'date', width: 110, align: 'center', ellipsis: { tooltip: true } },
  { title: '车牌', key: 'plate', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '区域', key: 'region', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '公司', key: 'company', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
  { title: '业务', key: 'business', width: 'auto', align: 'center', ellipsis: { tooltip: true } },
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
          [[vPermission, 'put/api/v1/total/update/ob']]
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
        <NButton
          v-permission="'post/api/v1/total/list/ob'"
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
      :get-data="api.getTotalListOb"
      :get-data-params="{ business: userStore.name }"
    >
      <template #queryBar>
        <QueryBarItem label="日期" :label-width="70">
          <n-date-picker
            v-model:formatted-value="queryItems.date"
            type="date"
            clearable
            placeholder="请选择日期"
            @update="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="车牌" :label-width="70">
          <NInput
            v-model:value="queryItems.plate"
            clearable
            placeholder="请输入车牌"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="是否对接" :label-width="70">
          <NSelect
            v-model:value="queryItems.docking_time_not_null"
            clearable
            placeholder="请选择"
            :options="[
              { label: '已对接', value: true },
              { label: '未对接', value: false },
            ]"
            @update:value="$table?.handleSearch()" style="width: 200px;"
          />
        </QueryBarItem>
        <QueryBarItem label="是否完成" :label-width="70">
          <NSelect
            v-model:value="queryItems.is_completed"
            clearable
            placeholder="请选择"
            :options="[
              { label: '已完成', value: true },
              { label: '未完成', value: false },
            ]"
            @update:value="$table?.handleSearch()"  style="width: 200px;"
          />
        </QueryBarItem>
      </template>
    </CrudTable>

    <!-- 编辑 弹窗 -->
    <CrudModal
      v-model:visible="modalVisible"
      :title="modalTitle"
      :loading="modalLoading"
      @save="handleSave"
    >
      <NForm
        ref="modalFormRef"
        label-placement="left"
        label-align="left"
        :label-width="80"
        :model="modalForm"
        :rules="addAPIRules"
      >
        <NFormItem label="备注" path="remark">
          <NInput v-model:value="modalForm.remark" clearable placeholder="请输入备注" />
        </NFormItem>
      </NForm>
    </CrudModal>
  </CommonPage>
</template>

