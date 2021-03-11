from to_pdf import hwp_to_pdf
from parse_pdf import parse_pdf

def main():
	print('START')

	hwp_to_pdf()
	print('FINISH hwp_to_pdf')

	parse_pdf()
	print('FINISH parse_pdf')


if __name__ == "__main__":
	main()