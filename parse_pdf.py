import os
import sys
import base64

import fitz

base_dir = os.path.dirname(os.path.abspath(__file__))

input_dir = os.path.join(base_dir, 'input')
output_dir = os.path.join(base_dir, 'output')

pdf_dir = os.path.join(input_dir, 'pdf')
png_dir = os.path.join(output_dir, 'png')
text_dir = os.path.join(output_dir, 'text')
xhtml_dir = os.path.join(output_dir, 'xhtml')

def replace_math(new_text):

    # Number
    new_text = new_text.replace('', '$0')
    new_text = new_text.replace('', '$1')
    new_text = new_text.replace('', '$2')
    new_text = new_text.replace('', '$3')
    new_text = new_text.replace('', '$4')
    new_text = new_text.replace('', '$5')
    new_text = new_text.replace('', '$6')
    new_text = new_text.replace('', '$7')
    new_text = new_text.replace('', '$8')
    new_text = new_text.replace('', '$9')

    # Alphabet
    new_text = new_text.replace('', 'a')
    new_text = new_text.replace('', 'b')
    new_text = new_text.replace('', 'c')
    new_text = new_text.replace('', 's')
    new_text = new_text.replace('', 'l')
    new_text = new_text.replace('', 'q')
    new_text = new_text.replace('', 'x')
    new_text = new_text.replace('', 'y')
    new_text = new_text.replace('', 'z')

    # ETC    
    new_text = new_text.replace('', '$+')
    new_text = new_text.replace('', '$-')
    new_text = new_text.replace('', '(')
    new_text = new_text.replace('', ')')
    new_text = new_text.replace('', '=')
    new_text = new_text.replace('', ':')
    new_text = new_text.replace('', '<')
    new_text = new_text.replace('', '>')
    new_text = new_text.replace('', '.')
    new_text = new_text.replace('', '/')
    new_text = new_text.replace('', '&#176;')
    new_text = new_text.replace('⇄', '&#8644;')
    new_text = new_text.replace('', '$분수')

    # Custom
    new_text = new_text.replace('이 책에 대한 모든 권리는 신지호 통합 연구소에 있으므로 무단으로 전재하거나 복제, 배포 할 경우 처벌받을 수 있습니다.', '')
    new_text = new_text.replace('Everything You Need', '')
    new_text = new_text.replace('신지호 화학 연구소', '')

    return new_text

def parse_pdf():

    # change directory to pdf directory
    os.chdir(pdf_dir)

    # pdf directory에 있는 모든 파일 탐색
    for file_name in os.listdir():

        # Absolute paths
        pdf_file_path = os.path.join(pdf_dir, file_name)
        png_sub_dir = os.path.join(png_dir, file_name[:-4])
        text_file_path = os.path.join(text_dir, file_name[:-4] + '.txt')

        # 이미지 저장할 directory 생성
        os.makedirs(png_sub_dir, exist_ok=True)

        # pdf 읽기
        pdf_document = fitz.open(pdf_file_path)

        # 모든 page 탐색
        pdf_text = ''
        for current_page in range(len(pdf_document)):
            image_count = 0

            pdf_dict = pdf_document[current_page].getText('dict')
            
            for tmp in pdf_dict['blocks']:
                if 'image' in tmp:
                    pdf_text += f'[[page{current_page}-{image_count}.png]]'
                    # print(f'[[page{current_page}-{image_count}.png]]')
                    image_count += 1
                else:
                    for tmp_2 in tmp['lines']:
                        for tmp_3 in tmp_2['spans']:
                            pdf_text += replace_math(tmp_3['text'])
                            for char in tmp_3['text']:
                                try:
                                    char = replace_math(char)
                                    print(char, end='')
                                except:
                                    print('$$', end='')
                        pdf_text += '\n'
                        # print()
                pdf_text += '\n'
                # print('\n')

            # 현재 page의 모든 image 탐색
            image_count = 0
            for image in pdf_document.getPageImageList(current_page):
                xref = image[0]
                pix = fitz.Pixmap(pdf_document, xref)

                png_file_path = os.path.join(png_sub_dir, f'page{current_page}-{image_count}.png')
                image_count += 1

                if pix.n < 5:  # this is GRAY or RGB
                    pass
                else:  # CMYK: convert to RGB first
                    pix = fitz.Pixmap(fitz.csRGB, pix)

                # write png file
                pix.writePNG(png_file_path)

                # pix 초기화
                pix = None

        with open(text_file_path, 'w', encoding='utf-8') as out_file:
            pdf_text = pdf_text
            out_file.write(pdf_text)
