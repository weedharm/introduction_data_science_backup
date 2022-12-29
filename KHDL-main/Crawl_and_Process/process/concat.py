import pandas as pd


def concat_df(files):
    list_data_frame = []
    for file in files:
        d = pd.read_csv('../crawl/' + file, encoding="utf8", sep="\t")
        try:
            d = d.drop(labels=["Producer"], axis=1)
        except:
            pass
        list_data_frame.append(d)
    df = pd.concat(list_data_frame).drop_duplicates()

    return df


def price(text):
    try:
        text = str(text).replace(".", "").replace("₫", "").replace(r'\s+', "")
        return int(text)
    except:
        return "None"


if __name__ == '__main__':
    # noi 3 dataframe
    files = ['Product_An_Phat.csv', 'Product_HNCom.csv', 'Product_Phong_Vu.csv']
    concat_df(files)

    data = concat_df(files)
    for item in ["CPU", 'DISK', 'RAM', 'DISPLAY']:
        data = data.loc[data[item] != 'None']
    data = data.loc[data["CPU"] != 'Microsoft SQ 2']
    data = data.loc[data["RAM"] != 'LPDDR4x 4266Mhz on board']
    data = data.dropna()
    data.to_csv("1.csv", encoding="utf8", sep="\t", index=False)
