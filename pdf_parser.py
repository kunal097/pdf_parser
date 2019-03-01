import pandas as pd
import pdftotree as pdf
import re


def text_coordinate(html):
    # print(len(html))
    # print(html)
    top_list = []
    bottom_list = []

    while 1:
        try:
            tr_pos = html.index('<tr>')
            tr_end = html.index('</tr>')
            temp = html[tr_pos + 4:tr_end]
            top = temp.index('top=')
            top_end = temp[top + 5:].index(' ')
            top_list.append(float(temp[top + 5:top + top_end]))
            bottom = temp.index('bottom=')
            bottom_end = temp[bottom + 8:].index(' ')
            bottom_list.append(float(temp[bottom + 8:bottom + bottom_end]))
            html = html[tr_end + 5:]
        except Exception as e:
            print(e)
            break

    df = pd.DataFrame()
    df['top'] = top_list
    df['bottom'] = bottom_list


    return df


def format_df(data):
    row = []
    td_match = re.compile('>[\d \w \s]*</td>')

    while 1:
        tr_start = int()
        tr_end = int()
        try:
            tr_start = data.index('<tr>')
            tr_end = data.index('</tr>')

            tr_con = data[tr_start + 4:tr_end]

            col = td_match.findall(tr_con)

            col = [''.join(i[1:].replace('</td>', '').split('\n')).lstrip()
                   for i in col]

            row.append(col)

            data = data[tr_end + 5:]
        except:
            break

    return pd.DataFrame(row)


def check_index(df):
    index = []
    for i in range(df.shape[0] - 1):
        bottom = float(df.loc[i].bottom)
        top_next = float(df.loc[i + 1].top)

        if int(abs(bottom - top_next)) < 4:
            index.append((i, i + 1))

    return index


def create_df(index, df):
    table = []
    for i, j in index:
        temp_df = df.iloc[[i, j], :]

        d_col = temp_df.columns
        n_row = []

        for c in d_col:
            cell = '\n'.join(list(temp_df[c]))
            n_row.append(cell)
        table.append(n_row)

    return pd.DataFrame(table)


def main():
    html = pdf.parse('PDFwork.pdf', html_path=None)

    df = format_df(html)

    cor_df = text_coordinate(html)

    index_list = check_index(cor_df)

    final_df = create_df(index_list, df)

    final_df.to_csv('final_data.csv')


if __name__ == '__main__':
    main()
