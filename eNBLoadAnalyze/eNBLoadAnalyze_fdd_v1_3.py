# -*- coding: utf-8 -*- 
#! python3

# ============================================================
# 作    者： 徐金鹏
# 邮    箱： 19807120073@139.com
# 函数功能：用于孝感TDD基站高负荷分析
# 函数输入：源文件请通过LTE-OMC中lipengfei名下的高负荷分析模板提取
# 函数输出：满足四个高负荷指标的TDD基站
# 若发现错误，或对代码有任何疑问，请联系上述邮箱！
# ============================================================

# Third-Party Dependencies: 
# pandas
# numpy
# xlrd
# xlwt
# openpyxl

import pandas as pd
import numpy as np
import xlrd, xlwt
import os, time

def eNBLoadAnalyzeFDD(srcFile) :

	if srcFile is None : 
		return -1


	# Function: Data selection
	def dataSelection(dataType):
		oriUpPRBSt = wb.sheet_by_name(oriStName[dataType])
		newUpPRBSt = newWb.add_sheet(newStName[dataType])

		rowNum = oriUpPRBSt.nrows
		startRow = 4
		meanCol = 8

		currRow = startRow
		# Row pointer of new sheet
		newRowPnt = 0

		# Copy headers to new sheet
		headerRow = 0
		while headerRow < startRow :
			headerCol = 0
			while  headerCol < meanCol + 1:
				newUpPRBSt.write(headerRow, headerCol, label = oriUpPRBSt.cell(headerRow, headerCol).value)
				headerCol = headerCol + 1

			newRowPnt = newRowPnt +1
			headerRow = headerRow + 1

		# Select data
		while currRow < rowNum :

			if oriUpPRBSt.cell(currRow, meanCol).value >= specs[dataType] :
				# If satisfied, copy row data to new sheet
				currCol = 0
				while currCol < meanCol + 1:
					newUpPRBSt.write(newRowPnt, currCol, label = oriUpPRBSt.cell(currRow, currCol).value)
					currCol = currCol + 1

				newRowPnt = newRowPnt + 1	
			currRow = currRow + 1

	# Function: Add high load date column
	def addHighLoadDateCol(oriDf):
		date = oriDf.pop("开始时间")
		newDate = []

		i = 0
		while i < len(date) :
        		time = date[i]
        		newTime = str(time)
        		newDate.append(newTime[0:10])
        		i = i + 1

		ser = pd.Series(newDate)
		oriDf["高负荷时间"] = ser
		return oriDf	


	# MAIN BEGINS HERE!!!!!!!!!!!!!!!!!!!
	ori = pd.read_excel(srcFile)

	# Create folder for temp files
	# Which usage is data selection
	tmpPath = "tmp/"
	tmpFile = tmpPath + "output.xlsx"
	if (os.path.exists(tmpPath)) :
		# remove tmp files of this application
		if (os.path.exists(tmpFile)) :
			os.remove(tmpFile)
	else :
		os.makedirs(tmpPath)
		
	writer = pd.ExcelWriter(tmpPath + "output.xlsx")

	src = addHighLoadDateCol(ori)
	src.head()	
	src["序号"] = src["序号"].astype("category")

	# UplinkPRB
	uplinkPRB = pd.pivot_table(src, index=["小区名称"], columns=["高负荷时间"], values=["[FDD]PUSCH资源利用率"], aggfunc=[np.mean], fill_value=0, dropna = True, margins=True, margins_name = "均值")
	uplinkPRB.to_excel(writer, sheet_name = "FDD_PUSCH资源利用率", index = ["小区名称"], encoding="utf_8_sig", header = True)

	# Cannot select the Column: Margin ?
	# uplinkPRBLoc = uplinkPRB.loc[uplinkPRB["均值"]>0.52, :]

	# DownlinkPRB
	downlinkPRB = pd.pivot_table(src, index=["小区名称"], columns=["高负荷时间"], values=["[LTE]PDSCH资源利用率"], aggfunc=[np.mean], fill_value=0, dropna = True, margins=True, margins_name = "均值")
	downlinkPRB.to_excel(writer, sheet_name = "FDD_PDSCH资源利用率", index = ["小区名称"], encoding="utf_8_sig", header = True)

	# PDCCHUsage
	PDCCHUsage = pd.pivot_table(src, index=["小区名称"], columns=["高负荷时间"], values=["PDCCH CCE资源使用率"], aggfunc=[np.mean], fill_value=0, dropna = True, margins=True, margins_name = "均值")
	PDCCHUsage.to_excel(writer, sheet_name = "PDCCH CCE资源使用率", index = ["小区名称"], encoding="utf_8_sig", header = True)

	# MaxRRC
	MaxRRC = pd.pivot_table(src, index=["小区名称"], columns=["高负荷时间"], values=["[FDD]最大的RRC连接建立个数"], aggfunc=[np.mean], fill_value=0, dropna = True, margins=True, margins_name = "均值")
	MaxRRC.to_excel(writer, sheet_name = "FDD_最大的RRC连接建立个数", index = ["小区名称"], encoding="utf_8_sig", header = True)

	writer.save()

	# ================Data Selection=====================
	# 由于pandas.DataFrame.loc() 不支持从生成的均值列中筛选，故手动筛选

	# Create new workbook
	wb = xlrd.open_workbook(tmpFile)
	newWb = xlwt.Workbook(encoding = "utf-8")

	oriStName = {"uplinkPRB" : "FDD_PUSCH资源利用率", "downlinkPRB" : "FDD_PDSCH资源利用率", "PDCCHUsage" : "PDCCH CCE资源使用率", "MaxRRC" : "FDD_最大的RRC连接建立个数"}
	newStName = {"uplinkPRB" : "FDD_PUSCH资源利用率", "downlinkPRB" : "FDD_PDSCH资源利用率", "PDCCHUsage" : "PDCCH CCE资源使用率", "MaxRRC" : "FDD_最大的RRC连接建立个数"}
	specs = {"uplinkPRB" : 0.52, "downlinkPRB" : 0.5, "PDCCHUsage" : 0.34, "MaxRRC" : 400}

	# Select data
	dataSelection("uplinkPRB")
	dataSelection("downlinkPRB")
	dataSelection("PDCCHUsage")
	dataSelection("MaxRRC")

	# Save selected data with date
	newWb.save("fdd_result_" + time.strftime("%y%m%d") + ".xls")

	# Clean up...
	os.remove(tmpFile)
	if not os.listdir(tmpPath) :
		os.rmdir(tmpPath)
		
	pyTmpPath = "__pycache__"
	if (os.path.exists(pyTmpPath)) :
		pyTmpFiles = os.listdir(pyTmpPath)
		for pyTmpFile in pyTmpFiles :
			pyTmpFilePath = os.path.join(pyTmpPath, pyTmpFile)
			if os.path.isdir(pyTmpFilePath) :
				os.rmdir(pyTmpFilePath)
			else :
				os.remove(pyTmpFilePath)
		os.rmdir(pyTmpPath)
		
	return 0


