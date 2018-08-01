import pandas as pd
import matplotlib.pyplot as plt


#this is just a little function to display the full Dataframe to check certain
def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


#this function cleans the data (the official PKS was pretty messy)
#sadly i did some of the cleaning in the python console and did not keep the code
#before i transformed it into a .csv

def prepare_data(df):
    df = df.drop(['1'])
    index = list(df.index.values)
    for key in index:
        key.replace('*', '0')

    key_value = list(df.Straftat)

    if len(key_value) == len(index):
        key_dict = {}
        for n in range(len(index)):
            dict1 = {index[n]: key_value[n]}
            key_dict.update(dict1)
    else:
        raise Exception('Dataframe mapping for key_value / index not possible')

    df = df.drop(columns=['Straftat'])

    return df, key_dict


def get_plot(df, key, entry, key_dict):
    label = key_dict[key]
    df2 = df.loc[key]
    df2 = df2.sort_values(ascending=False)[1:entry]

    #plt.figure(figsize=(20, 12.5))

    plt.figure(figsize=(16, 10))
    plt.subplots_adjust(bottom=0.3, right=0.9, top=0.9)
    plt.xlabel('Quelle: https://www.bka.de/SharedDocs/Downloads/DE/Publikationen/PolizeilicheKriminalstatistik/2017/Standardtabellen/Tatverdaechtige/STD-TV-16-T62-TV-Staatsangehoerigkeiten_excel.xlsx'
               '\nDatenlizenz Deutschland – "dl-de/by-2-0" – Version 2.0  www.govdata.de/dl-de/by-2-0 ',
               horizontalalignment='left', x=0.0, fontsize=8)

    ax = df2.plot(kind='bar', color='blue')
    ax.set_title(label+'\nTOP {}'.format(entry, weight='heavy'))
    ax.tick_params(axis='x', labelsize=10)
    rects = ax.patches

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height*1.01, int(height),
                ha='center', va='bottom', size=8, weight='normal')

    save_path = 'E:\\PKSplot\\' + key + '.png'
    save_path = save_path.replace('*', '0')
    plt.savefig(save_path, dpi=150, format='png')
    #plt.show()
    plt.close()

    #normalize the dataset
    dfn = df.apply(lambda x: (x / x[0])*10000)
    dfn2 = dfn.loc[key]
    deutsch = dfn.loc[key]['Deutschland']
    dfn2 = dfn2.sort_values(ascending=False)[0:entry]

    plt.figure(figsize=(16, 10))
    plt.subplots_adjust(bottom=0.3, right=0.9, top=0.9)
    plt.xlabel('\n\nQuelle: https://www.bka.de/SharedDocs/Downloads/DE/Publikationen/PolizeilicheKriminalstatistik/2017/Standardtabellen/Tatverdaechtige/STD-TV-16-T62-TV-Staatsangehoerigkeiten_excel.xlsx'
                '\nDatenlizenz Deutschland – "dl-de/by-2-0" – Version 2.0  www.govdata.de/dl-de/by-2-0 '
                '\nNormalisiert mit: https://www.destatis.de/DE/Publikationen/Thematisch/Bevoelkerung/MigrationIntegration/AuslaendBevoelkerung.html'
                '\nhttps://www-genesis.destatis.de/genesis/online/link/tabellen/12521*',
                horizontalalignment='left', x=0.0, fontsize=8)

    ax = dfn2.plot(kind='bar', color='blue')
    ax.set_title(label+'\nTOP {} '
                       '\nNormalisiert auf 100.000 Personen'
                       '\n Factor für Deutsche:{}'.format(entry, '{0:.2f}'.format(deutsch), weight='heavy'))
    ax.tick_params(axis='x', labelsize=10)
    rects = ax.patches

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height*1.01, "{0:.2f}".format(height),
                ha='center', va='bottom', size=8, weight='normal')

    save_path = 'E:\\PKSplot\\' + key +'_normalized.png'
    save_path = save_path.replace('*', '0')
    plt.savefig(save_path, dpi=150, format='png')
    plt.close()
    return


'''
keylist = ['0', '10000', '20010', '100000', '111000', '111100', '111200', '114000', '130000', '131000',
           '131700', '133000', '134000', '200000', '210000', '210050', '217000', '217010', '220000',
           '232500', '239000', '300000', '400000', '610000', '674000', '892000', '895000', '892500']

#for key in keylist:
    #get_plot(df, key, 20)
'''


#loading the csv

df = pd.read_csv('Straftaten_nach_Laender_mit_Anzahl.csv',
                 error_bad_lines=False,
                 sep=";", encoding="utf-8",
                 index_col='Key',
                 )


#first we need to clean and prepare the dataframe from the .csv
#prepare_data takes the Dataframe and returns the cleaned df and a map for the 'Straftaten' by Index

df, key_map = prepare_data(df)


#get plt needs the following arguments:
#(Dataframe(Pandas), Key(str), quantity to plot(int), the key_map(dict)
#get_plot(df, '216020', 20, key_map)

get_plot(df, '10000', 20, key_map)

