import { request } from '@/utils'
import { get, update } from 'lodash-es'

export default {
  login: (data) => request.post('/base/access_token', data, { noNeedToken: true }),
  getUserInfo: () => request.get('/base/userinfo'),
  getUserMenu: () => request.get('/base/usermenu'),
  getUserApi: () => request.get('/base/userapi'),
  // profile
  updatePassword: (data = {}) => request.post('/base/update_password', data),
  // users
  getUserList: (params = {}) => request.get('/user/list', { params }),
  getUserById: (params = {}) => request.get('/user/get', { params }),
  createUser: (data = {}) => request.post('/user/create', data),
  updateUser: (data = {}) => request.post('/user/update', data),
  deleteUser: (params = {}) => request.delete(`/user/delete`, { params }),
  resetPassword: (data = {}) => request.post(`/user/reset_password`, data),
  // role
  getRoleList: (params = {}) => request.get('/role/list', { params }),
  createRole: (data = {}) => request.post('/role/create', data),
  updateRole: (data = {}) => request.post('/role/update', data),
  deleteRole: (params = {}) => request.delete('/role/delete', { params }),
  updateRoleAuthorized: (data = {}) => request.post('/role/authorized', data),
  getRoleAuthorized: (params = {}) => request.get('/role/authorized', { params }),
  // menus
  getMenus: (params = {}) => request.get('/menu/list', { params }),
  createMenu: (data = {}) => request.post('/menu/create', data),
  updateMenu: (data = {}) => request.post('/menu/update', data),
  deleteMenu: (params = {}) => request.delete('/menu/delete', { params }),
  // apis
  getApis: (params = {}) => request.get('/api/list', { params }),
  createApi: (data = {}) => request.post('/api/create', data),
  updateApi: (data = {}) => request.post('/api/update', data),
  deleteApi: (params = {}) => request.delete('/api/delete', { params }),
  refreshApi: (data = {}) => request.post('/api/refresh', data),
  // depts
  getDepts: (params = {}) => request.get('/dept/list', { params }),
  createDept: (data = {}) => request.post('/dept/create', data),
  updateDept: (data = {}) => request.post('/dept/update', data),
  deleteDept: (params = {}) => request.delete('/dept/delete', { params }),
  // auditlog
  getAuditLogList: (params = {}) => request.get('/auditlog/list', { params }),
  // transactions
  getTransactionsList: (params = {}) => request.get('/transactions/list', { params }),
  getTransactionById: (params = {}) => request.get('/transactions/get', { params }),
  createTransaction: (data = {}) => request.post('/transactions/create', data),
  updateTransaction: (data = {}) => request.post('/transactions/update', data),
  deleteTransaction: (params = {}) => request.delete('/transactions/delete', { params }),
  // total
  getTotalList: (params = {}) => request.get('/total/list', { params }),
  getTotalById: (params = {}) => request.get('/total/get', { params }),
  getTotalListYyfs: (params = {}) => request.get('/total/list/yyfs', { params }),
  getTotalListBs: (params = {}) => request.get('/total/list/bs', { params }),
  createTotal: (data = {}) => request.post('/total/create', data),
  updateTotal: (data = {}) => request.post('/total/update', data),
  getTotalListOb: (params = {}) => request.get('/total/list/ob', { params }),
  updateTotalOb: (data = {}) => request.post('/total/update/ob', data),
  updateTotalYyfs: (data = {}) => request.post('/total/update/yyfs', data),
  deleteTotal: (params = {}) => request.delete('/total/delete', { params }),
  // field_work
  getFieldWorkList: (params = {}) => request.get('/field_work/list', { params }),
  getFieldWorkById: (params = {}) => request.get('/field_work/get', { params }),
  createFieldWork: (data = {}) => request.post('/field_work/create', data),
  updateFieldWork: (data = {}) => request.post('/field_work/update', data),
  deleteFieldWork: (params = {}) => request.delete('/field_work/delete', { params }),
  // duty_staff
  getDutyStaffList: (params = {}) => request.get('/duty_staff/list', { params }),
  getDutyStaffListfs: (params = {}) => request.get('/duty_staff/list_fs', { params }),
  getDutyStaffById: (params = {}) => request.get('/duty_staff/get', { params }),
  createDutyStaff: (data = {}) => request.post('/duty_staff/create', data),
  updateDutyStaff: (data = {}) => request.post('/duty_staff/update', data),
  deleteDutyStaff: (params = {}) => request.delete('/duty_staff/delete', { params }),
}
