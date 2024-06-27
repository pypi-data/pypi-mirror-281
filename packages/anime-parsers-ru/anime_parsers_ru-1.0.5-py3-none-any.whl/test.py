from anime_parsers_ru.parser_kodik import KodikParser

parser = KodikParser()

#print(shiki_id) # 2472

print(parser.get_link(
    id='z20', 
    id_type='shikimori', 
    seria_num=1, 
    translation_id='609'))