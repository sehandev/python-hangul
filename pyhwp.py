import os
import olefile

base_dir = os.path.dirname(os.path.abspath(__file__))
hwp_dir = os.path.join(base_dir, 'hwp')

hwp_file_path = os.path.join(hwp_dir, '02 지구와 생명체를 이루는 원소의 생성' + '.hwp')

def pyhwp_test():

	# olefile이 아니면 중단
	if not olefile.isOleFile(hwp_file_path):
		print(f'FAIL : {hwp_file_path} is not an ole file')
		return -1

	# hwp 읽기
	with olefile.OleFileIO(hwp_file_path) as ole:
		hwp_listdir = ole.listdir(streams=True, storages=False)
		print(hwp_listdir)
		if not ole.exists('\x05HwpSummaryInformation'):
			print(f'FAIL : {hwp_file_path} is not a hwp file')
			return -1

		# prv_text = ole.openstream('BodyText/Section0')
		prv_text = ole.openstream('\x05HwpSummaryInformation')
		text = prv_text.read()[:50]
		text = text.decode('utf-16')
		print(text)