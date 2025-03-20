<script setup>
import { h, onMounted, ref, resolveDirective, withDirectives } from 'vue'
import { NButton, NForm, NFormItem, NInput, NPopconfirm } from 'naive-ui'
import * as XLSX from 'xlsx'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import TheIcon from '@/components/icon/TheIcon.vue'

import { renderIcon } from '@/utils'
import { useCRUD } from '@/composables'
// import { loginTypeMap, loginTypeOptions } from '@/constant/data'
import api from '@/api'

defineOptions({ name: '交易记录管理' })

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')

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
  name: '交易记录',
  initForm: {},
  doCreate: api.createTransaction,
  doUpdate: api.updateTransaction,
  doDelete: api.deleteTransaction,
  refresh: () => $table.value?.handleSearch(),
})

onMounted(() => {
  $table.value?.handleSearch()
})

const exportToExcel = async () => {
  try {
    // 获取当前查询条件
    const queryParams = { ...queryItems.value, page: 1, page_size: 99999 }; // 设定一个足够大的 page_size 确保获取所有数据

    // 请求 API 获取所有符合条件的数据
    const response = await api.getTransactionsList(queryParams);

    // 确保返回的数据正确
    if (!response || !response.data || response.data.length === 0) {
      window.$message?.warning('无数据可导出');
      return;
    }

    // 处理数据，格式化为 Excel 需要的格式
    const data = response.data.map(row => ({
      '支付时间': row.payment_time,
      '支付金额': row.payment_amount,
      '收款人': row.recipient
    }));

    // 创建 Excel 工作表和工作簿
    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, '交易记录');

    // 生成并下载 Excel 文件
    XLSX.writeFile(wb, `交易记录_${new Date().toISOString().slice(0, 10)}.xlsx`);
  } catch (error) {
    console.error('导出 Excel 失败:', error);
    window.$message?.error('导出失败，请检查网络或稍后重试');
  }
}

async function handleRefreshApi() {
  $table.value?.handleSearch()
}

// 定义API表单验证规则
const addAPIRules = {
  payment_time: [
    {
      required: true,
      message: '请输入支付时间',
      trigger: ['input', 'blur', 'change']
    },
  ],
  payment_amount: [
    {
      required: true,
      message: '请输入支付金额',
      trigger: ['input', 'blur', 'change'],
      type: 'number',
    },
  ],
  recipient: [
    {
      required: true,
      message: '请输入收款人',
      trigger: ['input', 'blur', 'change'],
    },
  ],
}

// 定义表格列配置
const columns = [
  {
    title: '支付时间',
    key: 'payment_time',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '支付金额',
    key: 'payment_amount',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '收款人',
    key: 'recipient',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
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
              onClick: () => {
                handleEdit(row)
                modalForm.value.roles = row.roles.map((e) => (e = e.id))
              },
            },
            {
              default: () => '编辑',
              icon: renderIcon('material-symbols:edit', { size: 16 }),
            }
          ),
          [[vPermission, 'post/api/v1/transactions/update']]
        ),
        h(
          NPopconfirm,
          {
            onPositiveClick: () => handleDelete({ transaction_id: row.id }, false),
            onNegativeClick: () => {},
          },
          {
            trigger: () =>
              withDirectives(
                h(
                  NButton,
                  {
                    size: 'small',
                    type: 'error',
                    style: 'margin-right: 8px;',
                  },
                  {
                    default: () => '删除',
                    icon: renderIcon('material-symbols:delete-outline', { size: 16 }),
                  }
                ),
                [[vPermission, 'delete/api/v1/transactions/delete']]
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
  <!-- 业务页面 -->
  <CommonPage show-footer title="CURD示例 交易记录管理">
    <template #action>
      <div>
        <NButton
          v-permission="'post/api/v1/api/create'"
          class="float-right mr-15"
          type="primary"
          @click="handleAdd"
        >
          <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />新建记录
        </NButton>
        <NButton
          v-permission="'post/api/v1/api/refresh'"
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
    <!-- 表格 -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getTransactionsList"
    >
      <template #queryBar>
        <QueryBarItem label="支付时间" :label-width="70">
          <NInput
            v-model:value="queryItems.payment_time"
            clearable
            type="text"
            placeholder="请输入支付时间"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="支付金额" :label-width="70">
          <NInput
            v-model:value="queryItems.payment_amount"
            clearable
            type="text"
            placeholder="请输入支付金额"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="收款人" :label-width="70">
          <NInput
            v-model:value="queryItems.recipient"
            clearable
            type="text"
            placeholder="请输入收款人"
            @keypress.enter="$table?.handleSearch()"
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
      <NForm
        ref="modalFormRef"
        label-placement="left"
        label-align="left"
        :label-width="80"
        :model="modalForm"
        :rules="addAPIRules"
      >
        <NFormItem label="支付时间" path="payment_time">
          <!-- <NInput v-model:value="modalForm.payment_time" clearable placeholder="请输入支付时间" /> -->
          <n-date-picker v-model:formatted-value="modalForm.payment_time" type="datetime" clearable value-format="yyyy-MM-dd HH:mm:ss"/>
        </NFormItem>
        <NFormItem label="支付金额" path="payment_amount">
          <!-- <NInput v-model:value="modalForm.payment_amount" clearable placeholder="请输入支付金额" /> -->
          <n-input-number v-model:value="modalForm.payment_amount">
            <template #prefix>
              ￥
            </template>
          </n-input-number>
        </NFormItem>
        <NFormItem label="收款人" path="recipient">
          <NInput v-model:value="modalForm.recipient" clearable placeholder="请输入收款人" />
        </NFormItem>
      </NForm>
    </CrudModal>
  </CommonPage>
</template>
