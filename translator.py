import requests
import os
import chardet

API_KEY = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


def get_and_make_dirs():
    source = 'Source'
    result = 'Result'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_directory = os.path.join(current_dir, source)
    output_directory = os.path.join(current_dir, result)
    source_files = os.listdir(input_directory)
    os.mkdir(output_directory)

    return input_directory, output_directory, source_files


def translate_it(input_directory, output_directory, source_files, to_lang='ru'):
    for file in source_files:
        lang = file[:2]    # it takes name from file, e.g. "DE" to use it in names of output files
        result_files = os.path.join(input_directory, file)
        with open(result_files, 'rb') as f:
            data = f.read()
            result = chardet.detect(data)
            my_data = data.decode(result['encoding'])

            params = {
                'key': API_KEY,
                'text': my_data,
                'lang': to_lang,
            }

            response = requests.get(URL, params=params)
            json_ = response.json()
            full_text = ''.join(json_['text'])

            output_file = 'translation_from_{}_to_{}.txt'.format(lang, to_lang)
            output_files = os.path.join(output_directory, output_file)
            with open(output_files, 'w') as fl:
                fl.write(full_text)


def main():
    my_input_directory, my_output_directory, my_source_files = get_and_make_dirs()
    translate_it(my_input_directory, my_output_directory, my_source_files)


main()






