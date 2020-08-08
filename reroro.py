# ----------------------------------------------------------------
# 个人使用的夜神模拟器 明日方舟脚本库
# ----------------------------------------------------------------
'''
使用方法：
创造对象
sim1 = reroro(窗口名)

sim1.setAdbDevice(r' -s 127.0.0.1:62026 ')	# 设置adbshell的地址端口
'''

# ----------------------------------------------------------------
# 导入库
# ----------------------------------------------------------------
import time
import random
from cv2 import cv2
#import cv2
import numpy as np
import sys
import os
import json


# ----------------------------------------------------------------
# 全局变量
# ----------------------------------------------------------------
# 资源芯片每周日期表 剔除表
level_period_list = {
	'1':['ce', 'ca', 'pr-c', 'pr-d'],
	'2':['ap', 'sk', 'pr-a', 'pr-c'],
	'3':['ce', 'ap', 'pr-a', 'pr-b'],
	'4':['sk', 'ca', 'pr-b', 'pr-d'],
	'5':['ce', 'ap', 'pr-c', 'pr-d'],
	'6':['ca', 'pr-a'],
	'0':['sk', 'pr-b'],
}

# ----------------------------------------------------------------
# 全局函数
# ----------------------------------------------------------------
def dictSub(dict1, dict2):
	'''
	字典相减的函数 ，注意不要自己减自己，会出错
	'''
	for i in dict2:
		if i in dict1:
			dict1[i] = dict1[i] - dict2[i]
			if dict1[i] <= 0:
				dict1.pop(i)
	return dict1



# ----------------------------------------------------------------
# reroro 类
# ----------------------------------------------------------------
class reroro:
	'夜神模拟器的个人使用库，使用窗口名查找，adb输入'

	# 窗口名
	window_name = ''
	# 模拟器的adb程序路径
	nox_adb_path = r'V:\Nox\bin\nox_adb.exe '
	# 模拟器命令行工具
	nox_con_path = r'V:\Nox\bin\NoxConsole.exe '
	# 模拟器的shell地址和端口
	nox_adb_shell = r' -s 127.0.0.1:62026 '
	# 应用包名
	nox_app_name = r' com.hypergryph.arknights/com.u8.sdk.U8UnityContext '
	# 截取图片名
	cap_image_name = 'temp.png'
	# 图片匹配的阈值
	match_threshold = 0.7
	# debug模式开关
	DEBUG_MOD = False
	# 日志模式
	LOG_MOD = False
	# 干员替换位置列表
	replace_list = [(526, 105), (526, 455), 
					(706, 105), (706, 455), 
					(886, 105), (886, 455),
					(1066, 105), (1066, 455),
					(1246, 105), (1246, 455),
					(1426, 105), (1426, 455)]
	replace_size = [150, 335]
	# 信用交易所购买方块
	credits_list = [(337, 185), (652, 185), (967, 185), (1282, 185),
					(22, 500), (337, 500), (652, 500), (967, 500), (1282, 500)]
	credits_size = [295, 295]
	# 剿灭作战位置
	fight_exter_list = [(250, 400), (950, 700), (1350, 400)]
	# 关卡列表
	# jm是剿灭
	# pr-a 重装 医疗
	# pr-b 狙击 术士
	# pr-c 先锋 辅助
	# pr-d 近卫 特种
	level_list =   {'0-1':6,
					'0-2':6,
					'0-3':6,
					'0-4':6,
					'0-5':6,
					'0-6':6,
					'0-7':6,
					'0-8':6,
					'0-9':6,
					'0-10':6,
					'0-11':6,
					'1-1':6,
					'1-2':6,
					'1-3':6,
					'1-4':6,
					'1-5':6,
					'1-6':6,
					'1-7':6,
					'1-8':9,
					'ls-1':10,
					'ls-2':15,
					'ls-3':20,
					'ls-4':25,
					'ls-5':30,
					'sk-1':10,
					'sk-2':15,
					'sk-3':20,
					'sk-4':25,
					'sk-5':30,
					'ce-1':10,
					'ce-2':15,
					'ce-3':20,
					'ce-4':25,
					'ce-5':30,
					'jm-1':20,
					'jm-2':25,
					'jm-3':25,
					'pr-a-1':18,
					'pr-a-2':36,
					'pr-b-1':18,
					'pr-b-2':36,
					'pr-c-1':18,
					'pr-c-2':36,
					'pr-d-1':18,
					'pr-d-2':36,
					}
	# 物资筹备的关卡位置
	level_materials_list = {'1':(250, 720),
							'2':(600, 650),
							'3':(850, 500),
							'4':(1050, 370),
							'5':(1180, 230)}
	# 芯片搜索关卡位置
	level_chip_list = {'1':(482, 526),
					   '2':(1041, 327)}
	# 关卡图片列表
	level_img_list = {
		'0':[
			'0-1',
			'0-2',
			'0-3',
			'0-4',
			'0-5',
			'0-6',
			'0-7',
			'0-8',
			'0-9',
			'0-10',
			'0-11',
		],
		'1':[
			'1-1',
			'1-3',
			'1-4',
			'1-5',
			'1-6',
			'1-7',
			'1-8',
			'1-9',
			'1-10',
			'1-11',
			'1-12',
		],
		'2':[
			'2-1',
			'2-1s',
			'2-2',
			'2-2s',
			'2-3s',
			'2-4s',
			'2-3',
			'2-4',
			'2-5s',
			'2-6s',
			'2-7s',
			'2-5',
			'2-6',
			'2-7',
			'2-8s',
			'2-9s',
			'2-8',
			'2-9',
			'2-10s',
			'2-11s',
			'2-12s',
			'2-10',
		],
		'3':[
			'3-1',
			'3-2',
			'3-3',
			'tr-15',
			'3-1s',
			'3-2s',
			'3-4',
			'3-5',
			'3-6',
			'3-7',
			'3-3s',
			'3-8',
			'3-4s',
			'3-5s',
			'3-6s',
		],
		'4':[
			'4-1',
			'4-2',
			'4-3',
			'4-1s',
			'4-2s',
			'4-3s',
			'4-4',
			'4-5',
			'4-6',
			'4-4s',
			'4-5s',
			'4-6s',
			'4-7',
			'4-8',
			'4-9',
			'4-7s',
			'4-8s',
			'4-9s',
			'4-10s',
			'4-10',
		],
		'5':[
			'5-1',
			'5-2',
			'5-1s',
			'5-2s',
			'5-3',
			'5-4',
			'5-5',
			'5-6',
			'5-3s',
			'5-4s',
			'5-7',
			'5-8',
			'5-9',
			'5-5s',
			'5-6s',
			'5-7s',
			'5-10',
			'5-11',
			'5-1h',
		],
		'6':[
			'6-1',
			'6-2',
			'6-3',
			'6-4',
			'6-5',
			'6-7',
			'6-8',
			'tr-16',
			'6-9',
			'6-10',
			'6-1s',
			'6-2s',
			'6-11',
			'6-12',
			'6-14',
			'6-15',
			'6-3s',
			'6-4s',
			'6-16',
			'6-18',
			'6-1H',
		],
		'7':[
			'7-1',
			'7-2',
		]
	}
	# 升级符号
	is_level_up = False

	# ----------------------------------------------------------------
	# 图片库
	# ----------------------------------------------------------------
	img_lib = 'imglib/'
	# 应用图标
	img_name_app = 'app.png'
	# 开始游戏图片（黄色菱形）
	img_name_start_game = 'start_game.png'
	# 开始唤醒
	img_name_began_to_wake = 'began_to_wake.png'
	# 主页
	img_name_home_page_1 = 'home_page_1.png'
	img_name_home_page_2 = 'home_page_2.png'
	img_name_home_page_3 = 'home_page_3.png'
	# 公告
	img_name_notice = 'notice.png'
	# 获得物品
	img_name_get_item = 'get_item.png'
	# 每日签到
	img_name_day_check = 'day_check.png'
	# 在主页界面的基建提醒
	img_name_infrastructure_1 = 'infrastructure_1.png'
	img_name_infrastructure_2 = 'infrastructure_2.png'
	# 基建内的收获提示
	img_name_infrastructure_hint = 'infrastructure_hint.png'
	img_name_infrastructure_hint_white = 'infrastructure_hint_white.png'
	# 主页上的基建按钮
	img_name_infrastructure = 'infrastructure.png'
	# 一键收获
	img_name_harvest = 'harvest.png'
	# 菜单
	img_name_menu = 'menu.png'
	# 进驻总览
	img_name_presence_overview = 'presence_overview.png'
	# 进驻总览界面左上角的锚点图
	img_name_presence_overview_in = 'presence_overview_in.png'
	# 工作中的注意力涣散
	img_name_mind_lax_working = 'mind_lax_working.png'
	img_name_mind_lax_dorm = 'mind_lax_dorm.png'
	# 工作中
	img_name_in_working = 'in_working.png'
	# 在工作房间内
	img_name_in_facility = 'in_facility.png'
	img_name_in_facility_yellow = 'in_facility_yellow.png'
	# 制造厂黄色收取按钮
	img_name_in_facility_yellow_collect = 'in_facility_yellow_collect.png'
	img_name_in_dorm = 'in_dorm.png'
	# 作战界面 剿灭作战图标
	img_name_fight_exter = 'fight_exter.png'
	# 代理未勾选
	img_name_agency_not = 'agency_not.png'
	img_name_agency_yes = 'agency_yes.png'
	# 右下角蓝色开始行动
	img_name_blue_action = 'blue_action.png'
	img_name_red_action = 'red_action.png'
	img_name_action_over = 'action_over.png'
	img_name_level_up = 'level_up.png'
	img_name_reason_no_enough_1 = 'reason_no_enough_1.png'
	img_name_reason_no_enough_2 = 'reason_no_enough_2.png'
	# 剿灭作战结算图片
	img_name_exter_over = 'exter_over.png'
	# 物资筹备图片
	img_name_fight_resource = 'fight_resource.png'
	img_name_fight_resource_carbon = 'fight_resource_carbon.png'	# 碳关卡
	img_name_fight_resource_exper = 'fight_resource_exper.png'	# 经验本
	img_name_fight_resource_money = 'fight_resource_money.png'	# 钱本
	# 商店图片
	img_name_shop = 'shop.png'
	# 信用交易所
	img_name_credit_deal = 'credit_deal.png'
	img_name_credit_deal_white = 'credit_deal_white.png'
	# 信用交易所中的危机合约结算
	img_name_credit_deal_crisis_contract = 'credit_deal_crisis_contract.png'
	# 收取信用按钮
	img_name_reap_credit = 'reap_credit.png'
	# 已收取信用
	img_name_reap_credit_complete = 'reap_credit_complete.png'
	# 使用信用购买物品
	img_name_credit_buy_item = 'credit_buy_item.png'
	# 在宿舍的工作标签
	img_name_in_working_drom = 'in_working_drom.png'
	img_name_in_rest_drom = 'in_rest_drom.png'
	# 在会客室
	img_name_in_sitting_room = 'in_sitting_room.png'
	# 会客室线索号码
	img_name_sitting_room_number = [
		'sitting_room_1.png',
		'sitting_room_2.png',
		'sitting_room_3.png',
		'sitting_room_4.png',
		'sitting_room_5.png',
		'sitting_room_6.png',
		'sitting_room_7.png',
	]
	# 线索交流结束
	img_name_exchange_over = 'exchange_over.png'
	# 主页上的任务按钮
	img_name_mission = 'mission.png'
	# 每日任务未选中
	img_name_everyday_mission_unselected = 'everyday_mission_unselected.png'
	# 每日任务选中
	img_name_everyday_mission_selected = 'everyday_mission_selected.png'
	# 每周任务未选中
	img_name_everyweek_mission_unselected = 'everyweek_mission_unselected.png'
	# 每周任务选中
	img_name_everyweek_mission_selected = 'everyweek_mission_selected.png'
	# 任务列表点击领取
	img_name_get_mission = 'get_mission.png'
	# 任务完成图片
	img_name_mission_complete = 'mission_complete.png'
	# 干员招募
	# 开始招募干员按钮
	img_name_recruitment_of_agents_began = 'recruitment_of_agents_began.png'
	# 芯片搜索
	img_name_pr = 'pr.png'
	img_name_pr_a = 'pr_a.png'
	img_name_pr_b = 'pr_b.png'
	img_name_pr_c = 'pr_c.png'
	img_name_pr_d = 'pr_d.png'
	# 公开招募
	img_name_recruit = 'recruit.png'
	# 招募完成
	img_name_recruit_complete = 'recruit_complete.png'
	# 招募干员跳过
	img_name_get_agent_skip = 'get_agent_skip.png'
	# 招募干员-刷新标签
	img_name_flush_tag = 'flush_tag.png'
	# 招募干员-刷新标签-确认
	img_name_flush_tag_yes = 'flush_tag_yes.png'
	# 高资干员标签
	img_name_tag_high_senior_agent = 'tag_high_senior_agent.png'
	# 招募标签列表
	img_name_recruit_tag_list = [
		# 五星干员
		['tag_medical_agent.png', 'tag_support.png'],	# 医疗干员 支援		白面鸮 华法琳
		['tag_treat.png', 'tag_support.png'],			# 治疗 支援			白面鸮 华法琳
		['tag_support.png', 'tag_distant.png'],			# 支援 远程未		白面鸮 华法琳
		['tag_group_attack.png', 'tag_weaken.png'],		# 群攻 削弱			陨星
		['tag_weight_agent.png', 'tag_carry.png'],		# 重装干员 输出		雷蛇 火神
		['tag_carry.png', 'tag_protection.png'],		# 输出 防护			雷蛇 火神
		['tag_special_agent.png', 'tag_survival.png'],	# 特种干员 生存		狮蝎
		['tag_special_agent.png', 'tag_carry.png'],		# 特种干员 输出		崖心 狮蝎
		['tag_carry.png', 'tag_displace.png'],			# 输出 位移			崖心
		['tag_protection.png', 'tag_displace.png'],		# 防护 位移			可颂
		['tag_assist_agent.png', 'tag_carry.png'],		# 辅助干员 输出		真理
		['tag_carry.png', 'tag_slow_down.png', 'tag_distant.png'],	# 输出 减速 远程位	真理 夜魔
		['tag_assist_agent.png', 'tag_weaken.png'],		# 辅助干员 削弱		初雪
		['tag_weight_agent.png','tag_displace.png'],	# 重装干员 位移		可颂
		['tag_survival.png', 'tag_protection.png'],		# 生存 防护			火神
		['tag_survival.png', 'tag_weight_agent.png'],	# 生存 重装干员		火神
		['tag_summon.png'],								# 召唤				梅尔
		['tag_support.png', 'tag_const_recover.png'],	# 支援 费用回复		凛冬
		['tag_pioneer_agent.png', 'tag_support.png'],	# 先锋干员 支援		凛冬
		['tag_treat.png', 'tag_warlock_agent.png'],		# 治疗 术士干员		夜魔
		['tag_treat.png', 'tag_slow_down.png'],			# 治疗 减速			夜魔
		['tag_special_agent.png', 'tag_slow_down.png'],	# 特种干员 减速		食铁兽
		['tag_slow_down.png', 'tag_displace.png'],		# 减速 位移			食铁兽
		['tag_treat.png', 'tag_carry.png'],				# 治疗 输出			夜魔
		['tag_warlock_agent.png', 'tag_carry.png', 'tag_slow_down.png'],	# 术士 输出 减速		夜魔
		# 四星干员
		['tag_weaken.png'],								# 削弱				夜烟 流行
		['tag_special_agent.png'],						# 特种干员			砾 暗索 阿消
		['tag_quick_resurgence.png'],					# 快速复活			砾
		['tag_displace.png'],							# 位移				暗索 阿消
		['tag_survival.png', 'tag_snipe_agent.png'],	# 生存 狙击干员		杰西卡
		['tag_survival.png', 'tag_distant.png'],		# 生存 远程位		杰西卡
		['tag_snipe_agent.png', 'tag_slow_down.png'],	# 狙击干员 减速		白雪
		['tag_group_attack.png', 'tag_slow_down.png'],	# 群攻 减速			格雷伊 白雪
		['tag_carry.png', 'tag_slow_down.png'],			# 输出 减速			霜叶
		['tag_guards_agent.png', 'tag_slow_down.png'],	# 近卫干员 减速		霜叶
		['tag_near.png', 'tag_slow_down.png'],			# 近战位 减速		霜叶
		['tag_warlock_agent.png', 'tag_slow_down.png'],	# 术士干员 减速		格雷伊
		['tag_support.png'],							# 支援				杜宾
	]





	# 初始化函数
	def __init__(self, window_name):
		# 调试模式
		if self.DEBUG_MOD == True:
			if window_name == '':
				print('调试模式： 错误，未输入窗口名')

		self.window_name = window_name


	# ----------------------------------------------------------------
	# 库函数
	# ----------------------------------------------------------------

	# 启动模拟器
	def launchSim(self):
		command = self.nox_con_path + ' launch -name:' + self.window_name

		# debug模式
		if self.DEBUG_MOD == True:
			print(command)

		# 执行命令
		os.system(command)
	# 关闭模拟器
	def closeSim(self):
		command = self.nox_con_path + ' quit -name:' + self.window_name

		# debug模式
		if self.DEBUG_MOD == True:
			print(command)

		# 执行命令
		os.system(command)
	# 日志截图
	def capLogImage(self):
		# 进行模拟器截图
		self.simCap()
		# 取出截图图片
#		self.pullSimCap()
		# 计算当前时间
		localtime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) 
		# 生成日志图片名字
		log_img_name = self.window_name+'_' +localtime+'.png'
#		# 移动图片到日志文件夹
#		temp_img = open('./temp/'+self.cap_image_name, 'rb')
#		log_img = open('./log/'+log_img_name, 'wb')
#		log_img.write(temp_img.read())
#		temp_img.close()
#		log_img.close()
		# 将截图读取到日志文件夹
		self.pullSimCap(' /sdcard/'+self.cap_image_name+' '+'./log/'+log_img_name)


	# 获取模拟器截图，返回值是opencv格式图片
	def getSimCapImg(self):
		self.simCap()
		#time.sleep(1)
		self.pullSimCap()
		#time.sleep(2)
		img = cv2.imread('./temp/' + self.cap_image_name)
		return img


	# 模板匹配函数，在大图中找小图
	# 参数： img为大图，template为小图，rect是大图的切割框，method是匹配方法
	def matchTemplate(self, img, template, rect = None, method = cv2.TM_CCOEFF_NORMED):
		h, w = template.shape[:2]	# 获取小图的宽高

		# 如果有rect，则对大图进行切割
		if rect != None:
			img = img[rect[1][0]:rect[1][1], rect[0][0]:rect[0][1]]
			#print('进入了')

		# 进行图片匹配，获取匹配结果
		result = cv2.matchTemplate(img, template, method)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
		left_top = max_loc
		right_bottom = (left_top[0] + w, left_top[1] + h)

		if self.DEBUG_MOD == True:
			print(max_val, left_top, right_bottom)

			max_perc = max_val * 100			# 计算百分比
			font = cv2.FONT_HERSHEY_SIMPLEX		# 设置字体
			rect_color = (0, 255, 0)
			if max_perc < 50.0:		# 如果匹配率低于50% 匹配框颜色锁定为红色
				rect_color = (0, 0, 255)

			img_debug = img.copy()
			cv2.rectangle(img_debug, left_top, right_bottom, rect_color, 2)
			cv2.putText(img_debug, str(max_perc)[:4]+'%', (left_top[0], right_bottom[1]+20), font, 1, rect_color, 2, lineType=cv2.LINE_AA)
			cv2.namedWindow(self.window_name, 0)
			cv2.resizeWindow(self.window_name, 800, 450)
			cv2.imshow(self.window_name, img_debug)
			cv2.waitKey(1)

		return max_val, left_top, right_bottom

	# 模板匹配，自动对模拟器进行截图
	def matchTemplateEx(self, template, rect = [[0, 0], [0, 0]], method = cv2.TM_CCOEFF_NORMED):
		h, w = template.shape[:2]	# 获取小图的宽高

		img = self.getSimCapImg()

		# 如果有rect，则对大图进行切割
		if rect != [[0, 0], [0, 0]]:
			img = img[rect[1][0]:rect[1][1], rect[0][0]:rect[0][1]]
			#print('进入了')

		# 进行图片匹配，获取匹配结果
		result = cv2.matchTemplate(img, template, method)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
		left_top = max_loc
		right_bottom = (left_top[0] + w, left_top[1] + h)

		if self.DEBUG_MOD == True:
			print(max_val, left_top, right_bottom)

			max_perc = max_val * 100			# 计算百分比
			font = cv2.FONT_HERSHEY_SIMPLEX		# 设置字体
			rect_color = (0, 255, 0)
			if max_perc < 50.0:		# 如果匹配率低于50% 匹配框颜色锁定为红色
				rect_color = (0, 0, 255)

			cv2.rectangle(img, left_top, right_bottom, rect_color, 2)
			cv2.putText(img, str(max_perc)[:4]+'%', (left_top[0], right_bottom[1]+20), font, 1, rect_color, 2, lineType=cv2.LINE_AA)
			cv2.namedWindow(self.window_name, 0)
			cv2.resizeWindow(self.window_name, 800, 450)
			cv2.imshow(self.window_name, img)
			cv2.waitKey(1)

		return max_val, left_top, right_bottom

	def multiMatchTemplateEx(self, template, rect = [[0, 0], [0, 0]], method = cv2.TM_CCOEFF_NORMED, threshold = 0.92):
		h, w = template.shape[:2]	# 获取小图的宽高

		img = self.getSimCapImg()

		# 如果有rect，则对大图进行切割
		if rect != [[0, 0], [0, 0]]:
			img = img[rect[1][0]:rect[1][1], rect[0][0]:rect[0][1]]
			#print('进入了')

		# 进行图片匹配，获取匹配结果
		result = cv2.matchTemplate(img, template, method)
		#min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
		#left_top = max_loc
		#right_bottom = (left_top[0] + w, left_top[1] + h)
		loc = np.where(result >= threshold)
		val = []
		for pt in zip(*loc):
			right_bottom = (pt[1]+w, pt[0]+h)
			val.append((result[pt[0]][pt[1]], (pt[1], pt[0]), right_bottom))

		if self.DEBUG_MOD == True:
			print(val)

			for pos in val:
				max_perc = pos[0] * 100			# 计算百分比
				font = cv2.FONT_HERSHEY_SIMPLEX		# 设置字体
				rect_color = (0, 255, 0)
				if max_perc < 50.0:		# 如果匹配率低于50% 匹配框颜色锁定为红色
					rect_color = (0, 0, 255)

				cv2.rectangle(img, pos[1], pos[2], rect_color, 2)
				cv2.putText(img, str(max_perc)[:4]+'%', (pos[1][0], pos[2][1]+20), font, 1, rect_color, 2, lineType=cv2.LINE_AA)
			cv2.namedWindow(self.window_name, 0)
			cv2.resizeWindow(self.window_name, 800, 450)
			cv2.imshow(self.window_name, img)
			cv2.waitKey(1)

		return val
#		return max_val, left_top, right_bottom

	# 连续匹配图片
	# 参数： img为大图，template为小图，continuous连续匹配次数，threshold判断阈值，rect是大图的切割框，method是匹配方法,
	# 每次连续匹配减个1秒
	# 连续匹配成功后返回True
	def continMatchTemplate(self, template, threshold = 0.7, continuous = 1, rect = [[0, 0], [0, 0]], method = cv2.TM_CCOEFF_NORMED):

		continu_count = 0
		
		while True:
			# 进行图片截图
			#img = self.getSimCapImg()

			# 将图片进行匹配
			result = self.matchTemplateEx(template, rect, method)

			# 如果小于阈值，将连续判断计数重置为0
			if result[0] < threshold:
				continu_count = 0
			else:
				continu_count += 1

			# 计算计数，如果大于连续判断值，返回真值
			if continu_count >= continuous:
				return True

			# 调试模式
			if self.DEBUG_MOD == True:
				print('模板匹配结果', result)

			# 时间延迟1秒
			time.sleep(1)

	def waitMatchTemplateEx(self, template, threshold = 0.7, rect = [[0, 0], [0, 0]], method = cv2.TM_CCOEFF_NORMED):
		# 进行循环
		while True:
			# 进行图片匹配
			result = self.matchTemplateEx(template, rect, method)

			# 如果符合阈值
			if result[0] > threshold:
				return result




	# 通过颜色判断大图中的颜色值
	# img是大图，color_scope是颜色范围，包含两个HSV值的数组，类型是opencv的hsv类型
	def matchColorScope(self, img, color_scope, rect = None):
		# 检测是否输入范围
		if rect != None:
			img = img[rect[1][0]:rect[1][1], rect[0][0]:rect[0][1]]
		
		# 进行匹配
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, color_scope[0], color_scope[1])
		# 计算颜色匹配正确数量并计算比值
		img_true = np.size(mask[mask == 255])
		img_all = np.size(mask)
		img_scale = img_true/img_all

		# 调试模式
		if self.DEBUG_MOD:
			print(img_scale)	# 命令行输出结算比例值的结果

			# 将比例值转换成百分比
			img_scale_perc = img_scale * 100
			# 进行窗口图片输出
			font = cv2.FONT_HERSHEY_SIMPLEX
			font_color = (0, 255, 0)
			if img_scale_perc < 50.0:
				font_color = (0, 0, 255)
			# 开始输出窗口调试
			cv2.putText(img, str(img_scale_perc)[:4]+'%', (0, img.shape[0]), font, 1, font_color, 2, lineType=cv2.LINE_AA)
			cv2.namedWindow(self.window_name, 0)
			cv2.resizeWindow(self.window_name, 800, 450)
			cv2.imshow(self.window_name, img)
			cv2.waitKey(1)

		# 返回计算的比值
		return img_scale

	def matchColorScopeEx(self, color_scope, rect = None):
		'''颜色判断函数，自动判断模拟器截图界面'''
		
		# 获取模拟器截图
		img = self.getSimCapImg()

		# 进行颜色匹配
		result = self.matchColorScope(img, color_scope=color_scope, rect=rect)

		# 返回比例值
		return result


	def isMatchColorScopeEx(self, color_scope, rect = None, threshold = 0.5):
		'''返回布尔值的颜色匹配，需要输入占比例值'''
		if self.DEBUG_MOD:
			print('颜色判断, 颜色:', color_scope)
		
		# 进行颜色判断
		result = self.matchColorScopeEx(color_scope, rect=rect)

		# 进行比例值判断
		if result >= threshold:
			if self.DEBUG_MOD:
				print('判断目标大于颜色值')
			return True
		else:
			if self.DEBUG_MOD:
				print('判断目标小于颜色值')
			return False



	# 判断坐标点颜色是否匹配
	# 颜色使用RGB颜色
	# 坐标左上角为0，0，右下角为尺寸-1
	def matchColorPoint(self, img, color, point):
		# 将opencv默认BGR转换成RGB
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		# 判断颜色
		if img[point[0]][point[1]] == color:
			return True
		else:
			return False








	# 用adb截图模拟器
	# 截图到指定地址（模拟器内）
	def simCap(self, path = None):
		nox_cap_command = r' shell screencap '

		if path == None:
			path = r' -p /sdcard/' + self.cap_image_name + ' '
			if self.DEBUG_MOD:
				print(path)

		command = self.nox_adb_path + self.nox_adb_shell + nox_cap_command + path

		# 调试模式
		if self.DEBUG_MOD == True:
			print(command)
		# 执行命令
		os.system(command)

	# 将simCap截图到模拟器内的截图读取到电脑上
	def pullSimCap(self, path = None):
		nox_pull_command = r' pull '

		if path == None:
			path = r' /sdcard/' + self.cap_image_name + ' ' + './temp/' + self.cap_image_name

		command = self.nox_adb_path + self.nox_adb_shell + nox_pull_command + path

		# 调试模式
		if self.DEBUG_MOD == True:
			print(command)
		# 执行命令
		os.system(command)

	# 计算中心点，输入两个点
	def calcCentralPoint(self, left_top, right_bottom):
		pos = ((left_top[0]+right_bottom[0])/2, (left_top[1]+right_bottom[1])/2)
		return pos

	# 用adb模拟点击
	def clickMouseAdb(self, pos):
		nox_tap_command = r' shell input tap '

		command = self.nox_adb_path + self.nox_adb_shell + nox_tap_command + str(pos[0]) + ' ' + str(pos[1])

		# 调试模式
		if self.DEBUG_MOD == True:
			print(command)
		# 执行命令
		os.system(command)
	
	def clickMouseAdbCenter(self, left_top, right_bottom):
		'''模拟鼠标点击，自动计算中心点'''
		self.clickMouseAdb(self.calcCentralPoint(left_top, right_bottom))

	def swipeMouse(self, x1, y1, x2, y2, swipe_time = 1000):
		'''模拟器滑动'''
		nox_swipe_command = r' shell input swipe '

		command = self.nox_adb_path + self.nox_adb_shell + nox_swipe_command + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + ' ' + str(swipe_time)
		# 调试模式
		if self.DEBUG_MOD == True:
			print(command)
		# 执行命令
		os.system(command)
			
			





	## 设置应用默认位置
	#def setStartAppPos(self, app_pos):
	#	self.start_app_pos = list(app_pos)
	# 设置adb设备地址端口
	def setAdbDevice(self, device):
		self.nox_adb_shell = device

	# ----------------------------------------------------------------
	# 模块函数
	# ----------------------------------------------------------------
	def startApp(self):
		'''开始明日方舟APP'''
		start_app_command = r' shell am start -n '

		command = self.nox_adb_path + self.nox_adb_shell + start_app_command + self.nox_app_name

		# 调试模式
		if self.DEBUG_MOD == True:
			print(command)
		# 日志模式
		if self.LOG_MOD:
			self.capLogImage()
		# 执行命令
		os.system(command)

	# 开始游戏
	# 中间下面那个黄色按钮
	# 从打开应用知道进入主页
	def startGame(self):
		'''
		开始游戏
		中间下面那个黄色按钮
		从打开应用知道进入主页
		'''
		if self.waitIsApp():
			self.startApp()		# 启动明日方舟
			

		# 黄色菱形开始点击
		img_start_game = cv2.imread(self.img_lib+self.img_name_start_game)
		result = self.waitMatchTemplateEx(img_start_game)
		self.clickMouseAdb(self.calcCentralPoint(result[1], result[2]))

		# 开始唤醒，阿克奶次
		img_began_to_wake = cv2.imread(self.img_lib+self.img_name_began_to_wake)
		result = self.waitMatchTemplateEx(img_began_to_wake)
		self.clickMouseAdb(self.calcCentralPoint(result[1], result[2]))

	def loginHomePage(self):
		'''登录游戏主页后的判断逻辑'''
		# 判断公告和守夜
		if self.waitNoticeAndHomePage():
			time.sleep(5)
			if self.isNotice():
				self.clickMouseAdb((1547, 71))
				time.sleep(10)
			# 判断每日签到物品
			if self.isGetItem():
				self.clickMouseAdb((1547, 71))
				time.sleep(3)
				# 判断每日签到
				if self.waitIsDayCheck():
					self.clickMouseAdb((1503, 95))
					time.sleep(3)
			# 再次判断是否是公告
			if self.isNotice():
				self.clickMouseAdb((1547, 71))
				time.sleep(10)
		# 判断主页
		if self.waitIsHomePage():
			return True

	def disElectricQuantity(self):
		'''处理电量加速'''
		if self.waitIsMatchTemplateEx(self.img_name_presence_overview):
			time.sleep(4)
			# 点击制造厂
			self.clickMouseAdb((407, 400))
			time.sleep(4)
			# 等待确认进入室内
			self.waitIsMatchTemplateEx(self.img_name_in_facility_yellow)
			self.clickMouseAdb((325, 780))
			time.sleep(4)
			# 点击加速按钮
			self.clickMouseAdb((1525, 677))
			time.sleep(4)
			# 加大电量
			self.clickMouseAdb((1200, 420))
			time.sleep(4)
			# 点击确定
			self.clickMouseAdb((1183, 732))
			time.sleep(4)
			# 确认回到制造厂
			self.waitIsMatchTemplateEx(self.img_name_in_facility_yellow_collect)
			# 点击收取按钮
			self.clickMouseAdb((1420, 800))
			time.sleep(4)
			# 回到基建
			self.clickMouseAdb((120, 50))
			time.sleep(4)
			self.clickMouseAdb((120, 50))
			time.sleep(4)

	def disSittingRoom(self):
		'''处理会客室'''
		self.waitIsMatchTemplateEx(self.img_name_presence_overview)
		time.sleep(4)
		# 点击会客室
		self.clickMouseAdb((1472, 280))
		time.sleep(4)

		# 确认进入室内
		self.waitIsMatchTemplateEx(self.img_name_in_sitting_room)
		time.sleep(4)

		# 点击左下角
		self.clickMouseAdb((325, 780))
		time.sleep(4)
		
		# 判断是否线索交流结束
		result = self.isMatchTemplateEx(self.img_name_exchange_over)
		if result[0]:
			#self.clickMouseAdb((600, 50))
			self.clickMouseAdb((120, 50))
			time.sleep(4)

		# 领取线索
		self.clickMouseAdb((1500, 230))		# 点击每日线索
		time.sleep(4)
		self.clickMouseAdb((1000, 725))		# 领取线索
		time.sleep(4)
		self.clickMouseAdb((1235, 125))		# 关闭右上角
		time.sleep(4)
		self.clickMouseAdb((1500, 360))		# 领取好友线索
		time.sleep(4)
		self.clickMouseAdb((1350, 860))		# 点击领取
		time.sleep(4)
		self.clickMouseAdb((130, 800))		# 好友领取返回
		time.sleep(4)

		# 逐个点击号码
		for i_number in self.img_name_sitting_room_number:
			result = self.isMatchTemplateEx(i_number, threshold=0.85)
			if result[0]:
				self.clickMouseAdbCenter(result[1], result[2])
				time.sleep(2)
				self.clickMouseAdb((1350, 300))
				time.sleep(2)
		self.clickMouseAdb((130, 800))		# 返回
		time.sleep(4)

		# 是否可以解锁线索交流
		self.clickMouseAdb((875, 820))
		time.sleep(4)
		# 进行日志记录
		self.capLogImage()

		# 返回基建
		self.clickMouseAdb((120, 50))
		time.sleep(4)
		result = self.isMatchTemplateEx(self.img_name_presence_overview)
		if not result[0]:
			self.clickMouseAdb((120, 50))
			time.sleep(4)







	def disInfrastructure(self, tier, acceler = True):
		'''处理基建
		tier是基建地下层数'''

		# 进入基建前的判断
		if self.waitIsHomePage():
			if self.DEBUG_MOD == True:
				print('进入基建前的主页判断，判断成功')
			img_infrastructure = cv2.imread(self.img_lib+self.img_name_infrastructure)
			result = self.matchTemplateEx(img_infrastructure)
			if self.LOG_MOD:
				self.capLogImage()
			self.clickMouseAdbCenter(result[1], result[2])	# 点击
		time.sleep(2)

		# 判断是否进入了基建内部，利用左上角进驻总览判断
		self.waitIsMatchTemplateEx(self.img_name_presence_overview)
		time.sleep(10)

		# 基建提示
		if self.isInfrastructureHint()[0]:
			time.sleep(5)
			if self.DEBUG_MOD == True:
				print('寻找基建收获提示成功')
			result = self.isInfrastructureHint()
			if self.LOG_MOD:
				self.capLogImage()
			if result[0]:
				self.clickMouseAdbCenter(result[1], result[2])
			time.sleep(2)

			# 一键收获
			for i in range(0, 5):
				result = self.isHarvest()
				if result[0]:
					self.clickMouseAdbCenter(result[1], result[2])
					time.sleep(2)
			time.sleep(10)
			# 判断白色的一键收获，
			result = self.isInfrastructureHintWhite()
			if result[0]:
				self.clickMouseAdbCenter(result[1], result[2])
			time.sleep(2)
			# 判断左上角是否有进驻总览，没有的话就点击一下
			result = self.isMatchTemplateEx(self.img_name_presence_overview)
			if not result[0]:
				self.clickMouseAdb((150, 150))
				time.sleep(4)
			# 进行日志记录
			if self.LOG_MOD:
				self.capLogImage()

		# 电量加速
		if acceler:
			self.disElectricQuantity()

		# 处理会客室
		self.disSittingRoom()

		# 进驻总览
		result = self.waitIsMatchTemplateEx(self.img_name_presence_overview)
		if result[0]:
			self.clickMouseAdbCenter(result[1], result[2])
			time.sleep(2)

		# 开始进驻替换
		self.waitIsMatchTemplateEx(self.img_name_presence_overview_in)	# 等待回到进驻总览界面
		self.disFacility((850, 250), 5)
		self.waitIsMatchTemplateEx(self.img_name_presence_overview_in)	# 等待回到进驻总览界面
		self.disFacility((850, 450), 2)
		self.waitIsMatchTemplateEx(self.img_name_presence_overview_in)	# 等待回到进驻总览界面
		self.swipeMouse(800, 800, 800, 290, 5000)
		time.sleep(5)
		tier_count = tier + 1
		if tier_count > 4:
			tier_count = 4
		for i in range(1, tier_count):
			#for j in range(0, len(struct[i])):
			self.waitIsMatchTemplateEx(self.img_name_presence_overview_in)	# 等待回到进驻总览界面
			self.disFacility((840, 200), 3)
			self.waitIsMatchTemplateEx(self.img_name_presence_overview_in)	# 等待回到进驻总览界面
			self.disFacility((840, 400), 3)
			self.waitIsMatchTemplateEx(self.img_name_presence_overview_in)	# 等待回到进驻总览界面
			self.disFacility((840, 600), 1)
			self.waitIsMatchTemplateEx(self.img_name_presence_overview_in)	# 等待回到进驻总览界面
			self.disDorm()
			time.sleep(2)
			# 如果是第二层，办公室也调换一下
			if i == 2:
				self.swipeMouse(800, 800, 800, 580, 5000)
				time.sleep(5)
				self.waitIsMatchTemplateEx(self.img_name_presence_overview_in)	# 等待回到进驻总览界面
				self.disFacility((840, 800), 1)
				time.sleep(2)
				self.swipeMouse(800, 800, 800, -60, 10000)
				time.sleep(5)
			else:
				self.swipeMouse(800, 800, 800, -250, 10000)
				time.sleep(5)
			#self.disFacility((840, 800), struct[i][3])
			if self.DEBUG_MOD == True:
				print('层数：', i)
		# 处理最后一层的宿舍
		if tier == 4:
			self.disDorm((840, 750))

		#for i in range(1, len(struct[1:])+1):
		#	self.disFacility((840, 200), struct[])
#		self.clickMouseAdb((840, 200))
#		time.sleep(1)
#		self.clickMouseAdb((1470, 850))
#		time.sleep(1)
#
#		self.clickMouseAdb((840, 400))
#		time.sleep(1)
#		self.clickMouseAdb((1470, 850))
#		time.sleep(1)
#
#		self.clickMouseAdb((840, 600))
#		time.sleep(1)
#		self.clickMouseAdb((1470, 850))
#		time.sleep(1)
#
#		self.clickMouseAdb((840, 800))
#		time.sleep(1)
#		self.clickMouseAdb((1470, 850))
#		time.sleep(1)


		# 返回主页
		if self.waitIsMenu():
			result = self.isMenu()
			self.clickMouseAdbCenter(result[1], result[2])
			time.sleep(2)
			self.clickMouseAdb((115, 353))

	def calcTag(self):
		'''计算标签，返回是否有匹配和点击位置数组'''
		# 获取模拟器截图
		img = self.getSimCapImg()
		# 遍历列表，判断是否有符合的组合
		for i_tag_match in self.img_name_recruit_tag_list:
			# 判断列表组合
			result = self.matchTag(i_tag_match, img)
			if result[0]:
				# 如果匹配完成
				return result
		return result

			



		#	for i_tag in i_tag_match:
		#		# 判断标签是否存在
		#		result = self.isMatchTemplateEx(i_tag)
		#		# 如果有一个标签没有匹配到
		#		if not result[0]:
		#			# 退出循环 进入下一个标签匹配
		#			break
	def matchTag(self, tag_match, img):
		back_list = list()
		# 把匹配结果加入列表
		for i_tag in tag_match:
			#back_list.append(self.isMatchTemplateEx(i_tag, threshold=0.96))
			back_list.append(self.isMatchTemplate(img, i_tag, threshold=0.96))
		# 检测匹配结果是否全真
		for i_back in back_list:
			if not i_back[0]:
				return [False, back_list]
		# 如果全真，返回
		return [True, back_list]
		





	def disRecruit(self):
		'''招募干员模块'''
		# 点击招募干员按钮
		# 判断主页
		self.loginHomePage()
		result = self.isMatchTemplateEx(self.img_name_recruit)
		self.clickMouseAdbCenter(result[1], result[2])
		time.sleep(4)

		# 是否有招募完成
		result_complete = self.isMatchTemplateEx(self.img_name_recruit_complete)
		while result_complete[0]:
			# 点击完成招募干员
			self.clickMouseAdbCenter(result_complete[1], result_complete[2])
			time.sleep(4)

			# 获得干员操作过程
			result = self.waitIsMatchTemplateEx(self.img_name_get_agent_skip)
			self.clickMouseAdbCenter(result[1], result[2])
			time.sleep(4)
			self.clickMouseAdb((800, 450))
			time.sleep(4)

			# 再次点击招募完成位置，进入词条界面
			self.clickMouseAdbCenter(result_complete[1], result_complete[2])
			time.sleep(4)

			# 点满招募时长
			for i in range(0, 9):
				self.clickMouseAdb((566, 186))
				time.sleep(0.1)

			# 如果是日志模式，截取图片保存词条
			if self.LOG_MOD:
				self.capLogImage()

			# 进入词条循环
			while True:

				# 是否有高资干员标签
				result_high = self.isMatchTemplateEx(self.img_name_tag_high_senior_agent, threshold=0.95)
				# 如果有高资干员
				if result_high[0]:
					# 点击右下角关闭按钮，返回招募界面
					self.clickMouseAdb((1222, 811))
					time.sleep(4)
					break
				
				# 招募许可是否足够
				# 如果招募许可不够
				if not self.isMatchColorScopeEx(((99, 255, 255),(99, 255, 255)), [[629,749],[824,856]]):
					# 点击右下角关闭按钮，返回招募界面
					self.clickMouseAdb((1222, 811))
					time.sleep(4)
					break

				# 计算标签
				result = self.calcTag()
				# 是否有4星以上标签组合
				if result[0]:
					# 点击所有标签组合
					for i_click in result[1]:
						self.clickMouseAdbCenter(i_click[1], i_click[2])
					# 如果是日志模式，截取图片保存词条
					if self.LOG_MOD:
						self.capLogImage()
					# 点击招募按钮
					self.clickMouseAdb((1219, 728))
					time.sleep(4)
					break

				# 是否有刷新标签
				result = self.isMatchTemplateEx(self.img_name_flush_tag)
				# 如果有的话
				if result[0]:
					# 点击刷新按钮
					self.clickMouseAdbCenter(result[1], result[2])
					time.sleep(4)
					# 点击确认按钮
					result = self.isMatchTemplateEx(self.img_name_flush_tag_yes)
					self.clickMouseAdbCenter(result[1], result[2])
					time.sleep(4)
					# 点满招募时长
					for i in range(0, 9):
						self.clickMouseAdb((566, 186))
						time.sleep(0.1)
				# 如果没有的话
				else:
					# 点击招募按钮
					# 如果是日志模式，截取图片保存词条
					if self.LOG_MOD:
						self.capLogImage()
					self.clickMouseAdb((1219, 728))
					time.sleep(4)
					break
					
					

				


				# 招聘许可是否足够
				# 招聘许可足够，继续
				# 计算标签
				# 是否拥有4星以上组合
				# 拥有4星以上组合，点击组合标签
				
				# 点击招募按钮
				# 

			# 再次判断是否有招募完成
			result_complete = self.isMatchTemplateEx(self.img_name_recruit_complete)


		# 没有招募完成按钮了，返回主页
		self.backHomePage()



	def disFight(self, level, count, types = 'number', level_up_mod = False):
		'''作战模块
		level 是关卡的号
		type 是计数类型，number是次数，reason是理智
		level_up_mod 是升级模式，如果升级了再次调用，默认关闭
		
		返回值：
		返回值是一个字典，记录了成功作战的次数，格式是
		"关卡号":成功作战次数'''

		# 用于计算完成作战次数的返回变量
		fight_over_count = dict()
		succeed_count = 0

		# 计算作战进行次数
		m_count = 0
		if types == 'reason':
			m_count = int(count/self.level_list[level])
		else:
			m_count = count
		if self.DEBUG_MOD == True:
			print('作战次数:', m_count)
			

		# 判断主页
		if self.waitIsHomePage():
			# 进入作战界面
			self.clickMouseAdb((1200, 200))
		else:
			if self.DEBUG_MOD == True:
				print('作战模块： 没找到主页，无法开始')
		time.sleep(2)

		# 判断作战类型
		if level[0].isdigit():
			# 判断为正常数字关卡
			# 进行普通关卡作战
			succeed_count = self.fightMain(level, m_count)
		else:
			# 判断为其他关卡
			# 判断是否是物资关卡
			if (level[:2] == 'ls') or (level[:2] == 'ca') or (level[:2] == 'sk') or (level[:2] == 'ce'):
				# 判断为物资筹备
				# 进入物资筹备
				succeed_count = self.fightResource(level, m_count)
			# 判断是否是芯片关卡
			elif level[:2] == 'pr':
				# 判断为芯片关卡
				succeed_count = self.fightChip(level, m_count)
			# 判断是否是剿灭关卡
			elif level[:2] == 'jm':
				# 判断为剿灭关卡
				succeed_count = self.fightExter(int(level[3])-1, m_count)
		
		# 如果升级了，再进行一次
		if level_up_mod:
			if self.is_level_up:
				self.disFight(level, count, types, True)

		# 返回主页
		self.backHomePage()
		
		# 记录完成的关卡
		fight_over_count[level] = succeed_count
		return fight_over_count

		


	def fightMain(self, level, count):
		'''主线关卡模块'''

		# 判断当前章节图片
		result = self.isMatchTemplateEx('chapter'+level[0]+'.png')
		# 判断是否是目标章节图,没有就进行循环
		while not result[0]:
			# 寻找其他图
			for i_chapter in range(1, 8):
				# 判断图片
				result = self.isMatchTemplateEx('chapter'+str(i_chapter)+'.png')
				# 判断是否找到图片
				if result[0]:
					# 找到了图片，进行位置判断
					if i_chapter > int(level[0]):
						# 找到的锚点图大于目标图,向右拉，往左移动
						self.swipeMouse(800, 450, 1400, 450, 2000)
					elif i_chapter < int(level[0]):
						# 如果小于，向左拉，往右移动
						self.swipeMouse(800, 450, 200,  450, 2000)
					break
			
			# 滑动结束，再次判断目标图片
			result = self.isMatchTemplateEx('chapter'+level[0]+'.png')

		# 寻找章节循环结束，找到目标图片，点击进入关卡选择
		self.clickMouseAdbCenter(result[1], result[2])
		time.sleep(3)

		# 寻找当前关卡图
		result = self.isMatchTemplateEx(level+'.png', threshold=0.92)
		# 获取关卡list
		m_level_list = self.level_img_list[level[0]]
		# 判断是否找到了关卡图
		while not result[0]:
			# 没有找到关卡图，寻找其他锚点图
			for i_level in m_level_list:
				# 判断锚点图
				result = self.isMatchTemplateEx(i_level+'.png', threshold=0.92)
				# 是否找到锚点图
				if result[0]:
					# 找到锚点图，进行位置判断
					if self.level_img_list[level[0]].index(i_level) > self.level_img_list[level[0]].index(level):
						# 找到的锚点图大于目标图,向右拉，往左移动
						self.swipeMouse(800, 450, 1400, 450, 2000)
						# 削减关卡列表，减少判断时间
						m_level_list = self.level_img_list[level[0]][:self.level_img_list[level[0]].index(i_level)]
						# 反转列表方便减少时间
						m_level_list.reverse()
					elif self.level_img_list[level[0]].index(i_level) < self.level_img_list[level[0]].index(level):
						# 如果小于，向左拉，往右移动
						self.swipeMouse(800, 450, 200,  450, 2000)
						# 削减关卡列表，减少判断时间
						m_level_list = self.level_img_list[level[0]][self.level_img_list[level[0]].index(i_level):]
					break
			
			# 滑动结束，再次判断目标图片
			result = self.isMatchTemplateEx(level+'.png', threshold=0.9)

		# 寻找关卡结束，找到目标关卡图，点击
		self.clickMouseAdbCenter(result[1], result[2])
		time.sleep(3)

		# 进入作战
		succeed_count = self.agencyFight(count)

		# 返回成功作战次数
		return succeed_count











	def fightExter(self, number, count):
		'''剿灭作战模块
		0: 切尔诺伯格
		1: 龙门外环
		2: 龙门市区'''

		# 从作战界面跳转到剿灭界面
		result = self.isMatchTemplateEx(self.img_name_fight_exter)
		if result[0]:
			self.clickMouseAdbCenter(result[1], result[2])
		time.sleep(2)

		# 选择剿灭作战
		self.clickMouseAdb(self.fight_exter_list[number])
		time.sleep(2)
		# 进行剿灭作战
		succeed_count = self.agencyFight(count, True)
		
		# 返回成功作战次数
		return succeed_count

	def fightResource(self, level, count):
		'''资源筹备模块'''

		# 进入物资筹备
		result = self.isMatchTemplateEx(self.img_name_fight_resource)
		self.clickMouseAdbCenter(result[1], result[2])
		time.sleep(2)

		# 资源筹备分辨
		if level[:2] == 'ls':
			# 经验本
			result = self.isMatchTemplateEx(self.img_name_fight_resource_exper)
			if result[0]:
				self.clickMouseAdbCenter(result[1], result[2])
			else:
				self.swipeMouse(800, 450, 0, 450)
				time.sleep(4)
				result = self.isMatchTemplateEx(self.img_name_fight_resource_exper)
				self.clickMouseAdbCenter(result[1], result[2])
		if level[:2] == 'sk':
			# 碳关卡
			result = self.isMatchTemplateEx(self.img_name_fight_resource_carbon)
			if result[0]:
				self.clickMouseAdbCenter(result[1], result[2])
			else:
				self.swipeMouse(800, 450, 0, 450)
				time.sleep(4)
				result = self.isMatchTemplateEx(self.img_name_fight_resource_carbon)
				self.clickMouseAdbCenter(result[1], result[2])
		if level[:2] == 'ce':
			# 钱本
			result = self.isMatchTemplateEx(self.img_name_fight_resource_money)
			if result[0]:
				self.clickMouseAdbCenter(result[1], result[2])
			else:
				self.swipeMouse(800, 450, 0, 450)
				time.sleep(4)
				result = self.isMatchTemplateEx(self.img_name_fight_resource_money)
				self.clickMouseAdbCenter(result[1], result[2])
		time.sleep(2)

		# 关卡选择
		self.clickMouseAdb(self.level_materials_list[level[3]])
		time.sleep(2)

		# 进入作战
		succeed_count = self.agencyFight(count)

		# 返回成功作战次数
		return succeed_count

	def fightChip(self, level, count):
		'''芯片搜索模块'''

		# 进入进片搜索
		result = self.waitIsMatchTemplateEx(self.img_name_pr)
		self.clickMouseAdbCenter(result[1], result[2])
		time.sleep(2)

		# 芯片搜索分辨
		if level[3] == 'a':
			result = self.isMatchTemplateEx(self.img_name_pr_a)
			self.clickMouseAdbCenter(result[1], result[2])
		if level[3] == 'b':
			result = self.isMatchTemplateEx(self.img_name_pr_b)
			self.clickMouseAdbCenter(result[1], result[2])
		if level[3] == 'c':
			result = self.isMatchTemplateEx(self.img_name_pr_c)
			self.clickMouseAdbCenter(result[1], result[2])
		if level[3] == 'd':
			result = self.isMatchTemplateEx(self.img_name_pr_d)
			self.clickMouseAdbCenter(result[1], result[2])
		time.sleep(2)

		# 关卡选择
		self.clickMouseAdb(self.level_chip_list[level[5]])
		time.sleep(2)

		# 进入作战
		succeed_count = self.agencyFight(count)

		# 返回成功作战次数
		return succeed_count

		
		



	# 开始代理作战模块
	def agencyFight(self, count, exter = False):
		'''开始代理作战模块
		count： 作战次数
		exter： 表示剿灭 布尔类型'''

		for i in range(0, count):
			# 确认是否打开代理
			time.sleep(4)
			result = self.isMatchTemplateEx(self.img_name_agency_not)
			if result[0]:
				self.clickMouseAdbCenter(result[1], result[2])
				time.sleep(2)

			# 右下角蓝色开始行动
			result = self.waitIsMatchTemplateEx(self.img_name_blue_action)
			if result[0]:
				self.clickMouseAdbCenter(result[1], result[2])
				time.sleep(4)

			# 判断是否理智不够
			result1 = self.isMatchTemplateEx(self.img_name_reason_no_enough_1)
			result2 = self.isMatchTemplateEx(self.img_name_reason_no_enough_2)
			if result1[0] or result2[0]:
				# 理智不足，提前结束
				self.clickMouseAdb((974,721))
				# 关卡计数器
				i = i - 1
				break

			# 红色行动开始
			result = self.waitIsMatchTemplateEx(self.img_name_red_action)
			if result[0]:
				self.clickMouseAdbCenter(result[1], result[2])
				time.sleep(2)

			# 剿灭作战匹配
			if exter:
				result = self.waitIsMatchTemplateEx(self.img_name_exter_over)
				# 日志模式
				if self.LOG_MOD:
					self.capLogImage()
				time.sleep(4)
				if result[0]:
					self.clickMouseAdbCenter(result[1], result[2])
					time.sleep(4)

			# 行动结束与等级升级双重匹配
			result = self.waitIsMatchTowTemplateEx(self.img_name_action_over, self.img_name_level_up)
			time.sleep(10)
			# 检测等级提升
			result = self.isMatchTemplateEx(self.img_name_level_up)
			if result[0]:
				self.is_level_up = True
				self.clickMouseAdb(result[1])
				time.sleep(5)
			# 等待行动结束
			result = self.waitIsMatchTemplateEx(self.img_name_action_over)
			# 日志模式
			if self.LOG_MOD:
				self.capLogImage()
			self.clickMouseAdbCenter(result[1], result[2])

		# 返回成功运行次数
		return i+1

	def creditHarvest(self):
		'''进入商店收取信用，购买物品'''
		# 进入商店
		result = self.waitIsMatchTemplateEx(self.img_name_shop)
		self.clickMouseAdbCenter(result[1], result[2])
		time.sleep(4)

		# 进入信用交易所
		result = self.waitIsMatchTemplateEx(self.img_name_credit_deal)
		self.clickMouseAdbCenter(result[1], result[2])
		time.sleep(4)

		# 检测是否收取完成了
		result = self.isMatchTemplateEx(self.img_name_reap_credit_complete)
		if result[0]:
			# 收取完了，提前回主页
			self.backHomePage()
			return



		# 点击收取信用按钮
		result = self.waitIsMatchTemplateEx(self.img_name_reap_credit)
		self.clickMouseAdbCenter(result[1], result[2])
		result = self.waitIsMatchTemplateEx(self.img_name_get_item)
		self.clickMouseAdbCenter(result[1], result[2])
		# 判断是否有危机合约
		time.sleep(5)
		result = self.isMatchTemplateEx(self.img_name_credit_deal_crisis_contract)
		if result[0]:
			self.clickMouseAdb((100, 450))
			time.sleep(5)


		# 使用信用购买物品
		for i in self.credits_list:
			# 点击物品
			# 确认是否是信用交易所
			self.waitIsMatchTemplateEx(self.img_name_credit_deal_white)
			self.clickMouseAdbCenter(i, (i[0]+self.credits_size[0], i[1]+self.credits_size[1]))
			time.sleep(2)
			# 购买物品
			result = self.waitIsMatchTemplateEx(self.img_name_credit_buy_item)
			self.clickMouseAdbCenter(result[1], result[2])
			time.sleep(2)
			# 确认获取物品
			self.waitIsMatchTowTemplateEx(self.img_name_get_item, self.img_name_credit_buy_item)
			self.clickMouseAdb((100, 450))
			time.sleep(2)

		# 日志模式
		if self.LOG_MOD:
			self.capLogImage()

		# 收获完物品 返回主页
		self.backHomePage()

	def everydayMission(self):
		'''每日任务处理'''
		# 确认是否是主页
		self.waitIsHomePage()
		# 点开任务按钮
		result = self.waitIsMatchTemplateEx(self.img_name_mission)
		self.clickMouseAdbCenter(result[1], result[2])
		time.sleep(5)

		# 确实是否是未选中状态
		result = self.isMatchTemplateEx(self.img_name_everyday_mission_unselected)
		if result[0]:
			self.clickMouseAdbCenter(result[1], result[2])
			time.sleep(2)

		# 确认是选中状态
		result = self.waitIsMatchTemplateEx(self.img_name_everyday_mission_selected)

		# 开始连点领取任务
		self.conGetMission()

		# 日志模式
		if self.LOG_MOD:
			self.capLogImage()

		# 返回主页
		self.backHomePage()

	def everyweekMission(self):
		'''每周任务领取'''
		# 确认是否是主页
		self.waitIsHomePage()
		# 点开任务按钮
		result = self.waitIsMatchTemplateEx(self.img_name_mission)
		self.clickMouseAdbCenter(result[1], result[2])
		time.sleep(5)

		# 确实是否是未选中状态
		result = self.isMatchTemplateEx(self.img_name_everyweek_mission_unselected)
		if result[0]:
			self.clickMouseAdbCenter(result[1], result[2])
			time.sleep(2)

		# 确认是选中状态
		result = self.waitIsMatchTemplateEx(self.img_name_everyweek_mission_selected)

		# 开始连点领取任务
		self.conGetMission()

		# 日志模式
		if self.LOG_MOD:
			self.capLogImage()

		# 返回主页
		self.backHomePage()

		
		# 领取完了
	def conGetMission(self):
		'''连续领取任务'''
		# 点击领取任务
		while True:
			result1 = self.isMatchTemplateEx(self.img_name_get_mission)
			result2 = self.isMatchTemplateEx(self.img_name_get_item)
			result3 = self.isMatchTemplateEx(self.img_name_mission_complete, rect=[[30, 460], [160, 260]])

			# 判断是否还有东西点
			if result3[0]:
				break
			elif result1[0] or result2[0]:
				if result1[0]:
					self.clickMouseAdbCenter(result1[1], result1[2])
				if result2[0]:
					self.clickMouseAdbCenter(result2[1], result2[2])
			else:
				# 没有东西点了，就跳出循环
				break
			time.sleep(3)








	def backHomePage(self):
		'''返回主页的模块函数'''
		result = self.waitIsMatchTemplateEx(self.img_name_menu)
		if result[0]:
			self.clickMouseAdbCenter(result[1], result[2])
			time.sleep(2)
		else:
			if self.DEBUG_MOD == True:
				print('没有找到返回主页的按钮')
		self.clickMouseAdb((115, 353))
			



	


























































	def disFacility(self, pos, number):
		'''处理工作设施'''
		self.clickMouseAdb(pos)
		time.sleep(2)
		#result = self.isMultiMatchTemplateEx(self.img_name_mind_lax_working)
		#for i in result:
		#	if i[0]:
		#		self.clickMouseAdbCenter(i[1], i[2])
		#	time.sleep(1)
		
		# 判断是否在工作房间内
		self.waitIsMatchTemplateEx(self.img_name_in_facility)

		for i in range(0, number*2):
			self.clickMouseAdbCenter(self.replace_list[i], (self.replace_list[i][0]+self.replace_size[0], self.replace_list[i][1]+self.replace_size[1]))

		## 日志模式
		#if self.LOG_MOD:
		#	self.capLogImage()

		self.clickMouseAdb((1470, 850))
		time.sleep(1)

	def disDorm(self, pos = (840, 800)):
		'''处理宿舍'''
		self.clickMouseAdb(pos)
		time.sleep(2)
		# 等待是否进入宿舍
		self.waitIsMatchTemplateEx(self.img_name_in_dorm)
		img = self.getSimCapImg()
		# 新版 处理宿舍点击
		count = 10
		i = 0
		while i < count:
			# 判断当前计数干员是否处于工作中
			result = self.isMatchTemplate(img, self.img_name_in_working_drom, rect=[[self.replace_list[i][0], self.replace_list[i][0]+self.replace_size[0]], [self.replace_list[i][1], self.replace_list[i][1]+self.replace_size[1]]])
			result1 = self.isMatchTemplate(img, self.img_name_in_rest_drom, rect=[[self.replace_list[i][0], self.replace_list[i][0]+self.replace_size[0]], [self.replace_list[i][1], self.replace_list[i][1]+self.replace_size[1]]])
			#result = self.isMatchTemplateEx(self.img_name_in_working_drom, rect=[[self.replace_list[i][0], self.replace_list[i][0]+self.replace_size[0]], [self.replace_list[i][1], self.replace_list[i][1]+self.replace_size[1]]])
			if result[0] or result1[0]:
				# 如果计数小于12，增加1
				if count < 12:
					count = count + 1
			# 如果没有处于工作中
			else:
				# 点击干员
				self.clickMouseAdbCenter(self.replace_list[i], (self.replace_list[i][0]+self.replace_size[0], self.replace_list[i][1]+self.replace_size[1]))
			i = i + 1



		## 处理宿舍点击
		#result = self.isMultiMatchTemplateEx(self.img_name_mind_lax_dorm, rect=[[0, 1050], [0, 900]]) 
		#result_work = self.isMultiMatchTemplateEx(self.img_name_in_working_drom, rect=[[0, 1050], [0, 900]])
		#if self.DEBUG_MOD == True:
		#	print(result)
		#if result != False:
		#	click_count = 6-len(result)	# 注意力涣散的点击计数
		#	if result_work != False:
		#		click_count = click_count - len(result_work)
		#	for i in range(0, click_count):
		#		self.clickMouseAdbCenter(self.replace_list[i], (self.replace_list[i][0]+self.replace_size[0], self.replace_list[i][1]+self.replace_size[1]))
		#	result = self.isMultiMatchTemplateEx(self.img_name_mind_lax_dorm)
		#	for i in result:
		#		self.clickMouseAdbCenter(i[1], i[2])

		## 日志模式
		#if self.LOG_MOD:
		#	self.capLogImage()
		
		self.clickMouseAdb((1470, 850))
		time.sleep(1)



		

		




	def isMatchTemplate(self, img, template_name, rect = None, threshold = None):
		'''判断图片匹配，返回是否匹配，以及位置
		img 匹配源大图片
		template_name 模板图片名
		rect 对大图的截取
		threshold 判断阈值'''
		template = cv2.imread(self.img_lib+template_name)
		result = self.matchTemplate(img, template, rect=rect)
		m_threshold = self.match_threshold

		# 如果输入了判断阈值
		if threshold != None:
			m_threshold = threshold

		if result[0] >= m_threshold:
			if self.DEBUG_MOD:
				print('判断', template_name, '：成功')
			return True, result[1], result[2]
		else:
			if self.DEBUG_MOD:
				print('判断', template_name, '：失败')
			return False, result[1], result[2]



	
	def isMatchTemplateEx(self, img_name, rect = [[0, 0], [0, 0]], threshold = None):
		if self.DEBUG_MOD == True:
			print('判断', img_name)
		img = cv2.imread(self.img_lib+img_name)
		result = self.matchTemplateEx(img, rect=rect)
		m_threshold = self.match_threshold

		# 如果输入了判断值
		if threshold != None:
			m_threshold = threshold
		
		if result[0] > m_threshold:
			if self.DEBUG_MOD == True:
				print('判断', img_name, '：成功')
			return True, result[1], result[2]
		else:
			if self.DEBUG_MOD == True:
				print('判断', img_name, '：没找到')
			return False, result[1], result[2]

	def isMultiMatchTemplateEx(self, img_name, rect = [[0, 0], [0, 0]], method = cv2.TM_CCOEFF_NORMED, threshold = 0.92):
		if self.DEBUG_MOD == True:
			print('多个判断：', img_name)
		img = cv2.imread(self.img_lib+img_name)
		result = self.multiMatchTemplateEx(img, rect=rect, threshold=threshold)

		if len(result) == 0:
			if self.DEBUG_MOD == True:
				print('多个判断', img_name, '没找到')
			return False
		else:
			if self.DEBUG_MOD == True:
				print('多个判断', img_name, '找到', len(result), '个')
			val = []
			for i in result:
				val.append((True, i[1], i[2]))
			return val

		

	def waitIsMatchTemplateEx(self, img_name):
		'''等待匹配图片'''
		while True:
			result = self.isMatchTemplateEx(img_name)
			if result[0]:
				return result

	def waitIsMatchTowTemplateEx(self, img_name1, img_name2):
		'''双重等待图片匹配'''
		while True:
			result1 = self.isMatchTemplateEx(img_name1)
			result2 = self.isMatchTemplateEx(img_name2)
			if result1[0]:
				return result1
			if result2[0]:
				return result2
			time.sleep(10)

		

	def isMenu(self):
		'''判断菜单'''
		if self.DEBUG_MOD == True:
			print('判断菜单')
		
		img_menu = cv2.imread(self.img_lib+self.img_name_menu)
		result = self.matchTemplateEx(img_menu)

		if result[0] > self.match_threshold:
			if self.DEBUG_MOD == True:
				print('判断菜单：成功')
			return True, result[1], result[2]
		else:
			if self.DEBUG_MOD == True:
				print('判断菜单：失败')
			return False, result[1], result[2]
	def waitIsMenu(self):
		'''等待判断菜单'''
		while True:
			if self.isMenu()[0]:
				return True
			
	
	def isHarvest(self):
		'''判断基建一键收获提示'''
		if self.DEBUG_MOD == True:
			print('判断基建一键收获提示')
		
		img_harvest = cv2.imread(self.img_lib+self.img_name_harvest)
		result = self.matchTemplateEx(img_harvest)

		if result[0] > self.match_threshold:
			if self.DEBUG_MOD == True:
				print('判断基建一键收获提示：找到了')
			return True, result[1], result[2]
		else:
			if self.DEBUG_MOD == True:
				print('判断基建一键收获提示：没找到')
			return False, result[1], result[2]

	def waitIsHarvest(self):
		'''等待基建判断'''
		while True:
			if self.isHarvest()[0]:
				return True



	def isInfrastructureHint(self):
		'''判断基建内的收获提示'''
		if self.DEBUG_MOD == True:
			print('判断基建内的收获提示')

		img_infrastructure_hint = cv2.imread(self.img_lib+self.img_name_infrastructure_hint)
		result = self.matchTemplateEx(img_infrastructure_hint)

		if result[0] > self.match_threshold:
			if self.DEBUG_MOD == True:
				print('判断基建内的收获提示：找到了')
			return True, result[1], result[2]
		else:
			if self.DEBUG_MOD == True:
				print('判断基建内的收获提示：没找到')
			return False, result[1], result[2]

	def waitIsInfrastructureHint(self):
		'''等待判断基建内收获提示'''
		while True:
			if self.DEBUG_MOD == True:
				print('等待判断基建内收获提示')

			if self.isInfrastructureHint()[0]:
				if self.DEBUG_MOD == True:
					print('找到了基建内收获提示')
				return True

	def isInfrastructureHintWhite(self):
		'''判断基建内的收获提示'''
		if self.DEBUG_MOD == True:
			print('判断基建内的收获提示 白')

		img_infrastructure_hint_white = cv2.imread(self.img_lib+self.img_name_infrastructure_hint_white)
		result = self.matchTemplateEx(img_infrastructure_hint_white)

		if result[0] > self.match_threshold:
			if self.DEBUG_MOD == True:
				print('判断基建内的收获提示 白：找到了')
			return True, result[1], result[2]
		else:
			if self.DEBUG_MOD == True:
				print('判断基建内的收获提示 白：没找到')
			return False, result[1], result[2]

	def waitIsInfrastructureHintWhite(self):
		'''等待判断基建内收获提示'''
		while True:
			if self.DEBUG_MOD == True:
				print('等待判断基建内收获提示 白！')

			result = self.isInfrastructureHintWhite()
			if result[0]:
				if self.DEBUG_MOD == True:
					print('找到了基建内收获提示')
				return result

		
			




	
	def isApp(self):
		'''判断是否是APP'''
		if self.DEBUG_MOD == True:
			print('判断是否是APP')

		img_app = cv2.imread(self.img_lib+self.img_name_app)
		result = self.waitMatchTemplateEx(img_app)

		if result[0] > self.match_threshold:
			if self.DEBUG_MOD == True:
				print('判断是否是APP： 是APP！')
			return True
		else:
			if self.DEBUG_MOD == True:
				print('判断是否是APP： 不是APP！')
			return False

	# 
	def waitIsApp(self):
		'''等待判断APP'''
		while True:
			if self.DEBUG_MOD == True:
				print('等待判断APP')

			if self.isApp():
				if self.DEBUG_MOD == True:
					print('是APP!')
				return True
			

	def isHomePage(self):
		'''判断是否是主页'''
		img_home_page_1 = cv2.imread(self.img_lib+self.img_name_home_page_1)
		img_home_page_2 = cv2.imread(self.img_lib+self.img_name_home_page_2)
		img_home_page_3 = cv2.imread(self.img_lib+self.img_name_home_page_3)

		# 判断三个图片，如果都确认的话就是
		if self.matchTemplateEx(img_home_page_1)[0] > self.match_threshold and self.matchTemplateEx(img_home_page_2)[0] > self.match_threshold and self.matchTemplateEx(img_home_page_3)[0] > self.match_threshold:
			return True
		else:
			return False

	def waitIsHomePage(self):
		'''等待版的判断主页'''
		while True:
			if self.DEBUG_MOD == True:
				print('等待版的判断主页判断中')

			if self.isHomePage():
				return True


	def isNotice(self):
		'''判断是否是公告'''
		# top:bottom left:right
		img_rect = [[1500, 1600], [0, 120]]
		
		# DEBUG模式
		if self.DEBUG_MOD == True:
			print('判断是否是公告')

		# 检测公告
		img_notice = cv2.imread(self.img_lib+self.img_name_notice)
		result = self.matchTemplateEx(img_notice, img_rect)
		if result[0] > self.match_threshold:
			# DEBUG模式
			if self.DEBUG_MOD == True:
				print('判断是否是公告: 是公告！')
			return True
		else:
			# DEBUG模式
			if self.DEBUG_MOD == True:
				print('判断是否是公告: 不是公告！')
			return False

	# 等待版的判断公告
	def waitIsNotice(self):
		while True:
			if self.DEBUG_MOD == True:
				print('等待版的判断公告判断中')

			if self.isNotice():
				return True

	# 同时等待公告和首页和每日登录奖励
	def waitNoticeAndHomePage(self):
		while True:
			if self.DEBUG_MOD == True:
				print('等待公告和守夜')

			if self.isNotice() or self.isHomePage() or self.isGetItem():
				return True

	# 判断是否是获得物品
	def isGetItem(self):
		img_get_item = cv2.imread(self.img_lib+self.img_name_get_item)
		result = self.matchTemplateEx(img_get_item)
		if result[0] > self.match_threshold:
			return True
		else:
			return False

	# 等待版的判断获得物品
	def waitIsGetItem(self):
		while True:
			if self.DEBUG_MOD == True:
				print('等待版的判断获得物品判断中')

			if self.isGetItem():
				return True

	# 判断是否是每日签到
	def isDayCheck(self):
		# top:bottom left:right
		img_rect = [[1400, 1600], [0, 150]]
		
		# DEBUG模式
		if self.DEBUG_MOD == True:
			print('判断是否是每日签到')

		# 检测公告
		img_day_check = cv2.imread(self.img_lib+self.img_name_day_check)
		result = self.matchTemplateEx(img_day_check, img_rect)
		if result[0] > self.match_threshold:
			# DEBUG模式
			if self.DEBUG_MOD == True:
				print('判断是否是每日签到: 是每日签到！')
			return True
		else:
			# DEBUG模式
			if self.DEBUG_MOD == True:
				print('判断是否是每日签到: 不是每日签到！')
			return False

	# 等待版的判断每日签到
	def waitIsDayCheck(self):
		while True:
			if self.DEBUG_MOD == True:
				print('等待版的判断获得每日签到判断中')

			if self.isDayCheck():
				return True

		







		



# ----------------------------------------------------------------
# main测试函数
# ----------------------------------------------------------------
def fullRun(argv, credit_mod = True, infrast_mod=True, debugmod=False):
	'''运行一套完整的模拟器运行'''
	# 创建模拟器对象
	sim = reroro(argv['name'])
	sim.setAdbDevice(argv['device'])
	sim.cap_image_name = sim.window_name+'.png'

	# debug模式与日志模式 修改点5-1
	sim.DEBUG_MOD  = True
	sim.LOG_MOD = True
	# 记录战斗的变量，字典
	fight_over_count = dict()

	# 启动模拟器
	sim.launchSim()
	time.sleep(100)
	# 启动游戏
	sim.startGame()
	# 确认登录
	sim.loginHomePage()

	# 进行作战
	for i_level in argv['level']:
		if argv['types'] == 'reason':
			fight_temp = sim.disFight(i_level, argv['level'][i_level], types='reason')
			fight_over_count = dict(fight_over_count, **fight_temp)
		else:
			fight_temp = sim.disFight(i_level, argv['level'][i_level])
			fight_over_count = dict(fight_over_count, **fight_temp)

	# 进行基建
	if infrast_mod:
		sim.disInfrastructure(argv['tier'], argv['acceler'])

	# 处理招募干员
	sim.disRecruit()

	# 处理信用
	if credit_mod:
		sim.creditHarvest()

	# 进行任务奖励领取
	sim.everydayMission()
	sim.everyweekMission()

	# 截图日志
	sim.capLogImage()

	# 全部完成 关闭模拟器
	sim.closeSim()

	# 返回战斗成功字典
	print(fight_over_count)
	return fight_over_count

def main():
	# name： 设备名
	# device： adb的连接IP
	# infrast： 基建的各个设施等级

	# 调试模式
	DEBUG_MOD = True


	while True:
		# 获取当前小时数
		time_hour = int(time.strftime('%H'))
		time_week = time.strftime('%w')
		#time_ap = time.strftime('%p').lower()

		# 修改点4-2
		if (time_hour >= 4) and (time_hour < 18):
			time_ap = 'am'
		else:
			time_ap = 'pm'


		if DEBUG_MOD:
			print('当前时间', time_hour)
		
		# 如果当前时间为 6点到8点 或 18点到20点，进行运作 修改点4-1
		if time_hour in [6, 7, 8, 18, 19, 20]:
			# 读取json设置
			json_file = open('config.json', 'r', encoding='utf-8')
			json_conf = json_file.read()
			json_file.close()
			print(json_conf)
			accounts_list = json.loads(json_conf)
			if DEBUG_MOD:
				print(json.dumps(accounts_list, ensure_ascii=False, indent=4))
			# 每个帐号循环
			for acc in accounts_list:
				# 将要进行的关卡写入level
				accounts_list[acc]['level'] = accounts_list[acc]['levels'][time_week][time_ap]
				accounts_list[acc]['level'] = dict(accounts_list[acc]['level'], **accounts_list[acc]['todo'])

				# 因为现在全面开放，剔除功能暂时关闭
				# 处理level,不符合星期的关卡被剔除
				temp_acc_list = accounts_list[acc]['level'].copy()
				for i_level in accounts_list[acc]['level']:
					# 获取当天应当剔除的列表
					level_period = level_period_list[time_week]
					# 如果关卡在当天剔除列表中，则剔除
					if i_level[:2] in level_period:
						temp_acc_list.pop(i_level)
					if i_level[:4] in level_period:
						temp_acc_list.pop(i_level)
				# 剔除完成，将剔除结果赋值给原字典
				accounts_list[acc]['level'] = temp_acc_list

				# 调试模式，打印处理过的level
				if DEBUG_MOD:
					print(accounts_list[acc]['level'])
				# 开始运行模拟器
				fight_over_count = fullRun(accounts_list[acc], debugmod=True)
				# 将已完成的关卡在todo列表中减去
				accounts_list[acc]['todo'] = dictSub(accounts_list[acc]['todo'], fight_over_count)
				accounts_list[acc]['over'] = fight_over_count
				#thread_fullRun = threading.Thread(target=fullRun, args=(accounts_list[acc]))
				#thread_fullRun.start()
				
				# 将json配置重新写入
				# 运行完一个帐号就写入一次，免得多个帐号中断影响记录
				json_conf = json.dumps(accounts_list, ensure_ascii=False, indent=4)
				json_file = open('config.json', 'w', encoding='utf-8')
				print(json_conf)
				json_file.write(json_conf)
				json_file.close()
				
				# 等待间隔
				#time.sleep(1800)
				#time.sleep(600)

			# 停止一些时间，防止本次时间范围内再次运行，等待下次 修改点4-3
			time.sleep(14400)

		time.sleep(600)




		

	


def test():
	sim = reroro('w')
	sim.setAdbDevice(' -s 127.0.0.1:62028 ')
	sim.cap_image_name = sim.window_name+'.png'
	sim.DEBUG_MOD  = True
	sim.LOG_MOD = True
	#sim.getSimCapImg()
	sim.disSittingRoom()
	#sim.disInfrastructure(3)
	#sim.agencyFight(6)
	#sim.disInfrastructure(4)
	#sim.loginHomePage()
	#sim.disRecruit()
	#sim.agencyFight(5)
	#sim.simCap()
	#sim.pullSimCap()
	#sim.agencyFight(5)
	#sim.agencyFight(6, exter=True)
	#sim.isMatchColorScopeEx(((99, 255, 255),(99, 255, 255)), [[629,749],[824,856]])

	#sim.disRecruit()
	#sim.calcTag()
	#sim.disDorm()
	#sim.agencyFight(2)
	#sim.disFight('jm-1',1)
	
	
	
#	json_file = open('config.json', 'r', encoding='utf-8')
#	json_conf = json_file.read()
#	json_file.close()
#	accounts_list = json.loads(json_conf)
#	accounts_list['acc1']['level'] = accounts_list['acc1']['levels']['1']['am']
#	# 开始运行模拟器
#	#fullRun(accounts_list[acc], debugmod=True, credit_mod=credit_mod)
#	fullRun(accounts_list['acc1'])
	

	
		
	


if __name__ == "__main__":
	main()
	#test()