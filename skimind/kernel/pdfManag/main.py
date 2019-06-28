# pdf data extractor
from . import data_extractor


# interfacedb
from . import interfacedb

# tools
from . import tools

# page split
from . import page_spliter


def bet_file_manag(filename, numlist, date_format, flag, *args, **kwargs):
    """
        traite les donnees contenues dans un fichier de type resultat
        et sauvegarde les donnees dans la database
    """
    # metadata acquire
    bet_object = BetDataTreatement(
                                    filename=filename, 
                                    numlist=numlist, 
                                    date_format=date_format, 
                                    flag=flag
                                )
    metadatas = get_meta_data()

    if metadatas:
        for datas in metadatas:
            interfacedb.config.request_object.save_matchs(datas)


def result_file_manag(filename, numlist, date_format, flag, *args, **kwargs):
    """
        traite les donnees contenues dans un fichier de type resultat
        et sauvegarde les donnees dans la database
    """
    # metadata acquire
    bet_object = ResultDataTreatement(
                                    filename=filename, 
                                    numlist=numlist, 
                                    date_format=date_format, 
                                    flag=flag
                                )
    metadatas = get_meta_data()

    if metadatas:
        for datas in metadatas:
            interfacedb.config.request_object.save_resultat(datas)

def pdf_process(filename:str, numlist:list=[], is_betfile=True, date_format=None):
    def split_date_and_serial(tablist):
        datetime = tablist[1]

        datetime_tab = datetime.split(" ")

        if len(datetime_tab) != 2:
            datetime_tab.append("00:00")
        
        datetime_tab[0] = tools.serialize_date_format(datetime_tab[0])
        
        return [tablist[0], *datetime_tab, *tablist[2:]]
    
    def insert_data_into_matchs(metadata, numlist_tag):
        for data in metadata:
            datas.insert(0, numlist_tag)
            interfacedb.config.request_object.save_matchs(datas)
    
    def insert_data_into_resultat(metadata, numlist_tag):
        for datas in metadata:
            # exclude time team-name classement
            # idmatch, date, resultats
            datas = [numlist_tag, *datas[:2], datas[7:]]

            interfacedb.config.request_object.save_matchs(datas)

    
    pages_nb = tools.count_pages(filename=filename)

    pages_list = [filename]
    
    if pages_nb > 1:
        pages_list = page_spliter.PDFsplit(pdf=filename)
    
    # pages iterators
    for filename in pages_list:
        metadata = data_extractor.pdf_data_process(filename=filename, is_betfile=is_betfile)

        # split date and time and serialize date
        metadata = map(split_date_and_serial, metadata)