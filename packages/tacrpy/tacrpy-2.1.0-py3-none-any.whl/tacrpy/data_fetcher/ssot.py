import pandas as pd

from google.cloud import bigquery
from google.oauth2 import service_account


class Projects:
    def __init__(self):
        """ Kontstruktor, který načte data do DataFrame, očistí finanční hodnoty a vytvoří agregovanou tabulku.
        """
        self.projects = self._get_projects()
        self._finance_cleaning('Náklady celkem')
        self._finance_cleaning('Podpora celkem')
        self._finance_cleaning('Ostatní celkem')
        self.summary = self.create_summary()

    def _get_projects(self) -> pd.DataFrame:
        """ Načte data o projektech ze "zdroje pravdy" z googlesheets uloženého na Google disku.
        Lze použít pouze v rámci Google Colab prostředí.

        :return: DataFrame načtených dat ze zdroje
        """
        credentials = service_account.Credentials.from_service_account_file(
            '/content/drive/Shareddrives/Analytické oddělení/Data/Zdrojová data/data-poc-424211-81ef80050634.json')
        project_id = 'data-poc-424211'
        client = bigquery.Client(credentials=credentials, project=project_id)

        query = """
        SELECT *
        FROM `data-poc-424211.ssot_test.projekty_ssot`
        """
        df = client.query(query).to_dataframe()
        return df

    def _finance_cleaning(self, column_name: str):
        """ Interní funkce, která očistí finanční data.

        :param column_name: název sloupce, ve kterém se mají finanční data očistit
        """

        self.projects[column_name].fillna(0, inplace=True)
        self.projects[column_name] = self.projects[column_name].str.replace(',', '.')
        self.projects[column_name] = self.projects[column_name].replace('', '0')
        self.projects[column_name] = self.projects[column_name].astype(float)

    def create_summary(self, level: str = 'cfp') -> pd.DataFrame:
        """ Vytvoří agregovaný souhrn buď na úrovni veřejných soutěží (defaultní) nebo na úrovni programů.

        :param level: určuje, na jaké úrovni se provede agregace

                      * 'cfp' (defaultní) - na úrovni veřejných soutěží
                      * 'prog' - na úrovni programů
        :return: agregovaný DataFrame, který obsahuje:

                * Počet podaných projektů
                * Počet podpořených projektů
                * Náklady podpořených projektů
                * Podpora podpořených projektů
        """
        if level not in ['cfp', 'prog']:
            raise ValueError('Neexistující forma agregace.')

        temp_df = self.projects.copy()
        temp_df['Podpořené'] = temp_df.apply(
            lambda x: 'Ano' if x['Fáze projektu'] in ['Realizace', 'Implementace', 'Ukončené'] else 'Ne', axis=1)
        submitted = temp_df.groupby(['Kód programu', 'Kód VS']).agg(
            {'Kód projektu': 'count', 'Náklady celkem': 'sum', 'Podpora celkem': 'sum'}).reset_index()
        funded = temp_df[temp_df['Podpořené'] == 'Ano'].groupby(['Kód programu', 'Kód VS']).agg(
            {'Kód projektu': 'count', 'Náklady celkem': 'sum', 'Podpora celkem': 'sum'}).reset_index()

        summary_df = pd.merge(submitted[['Kód programu', 'Kód VS', 'Kód projektu']], funded, how='inner',
                              on=['Kód programu', 'Kód VS'])
        summary_df.columns = ['Kód programu', 'Kód VS', 'Podané', 'Podpořené', 'Náklady', 'Podpora']

        if level == 'cfp':
            pass
        elif level == 'prog':
            summary_df = summary_df.groupby('Kód programu').agg('sum', numeric_only=True).reset_index()

        return summary_df

    def select_programme(self, *args: str) -> 'Projects':
        """ Vyfiltruje tabulku tak, aby obsahovala pouze projekty vybraných programů.

        :param args: kódy programů, které se mají vyfiltrovat
        :return: nová instance třídy Projects s vyfiltrovanými údaji
        :raise: ValueError
        """

        existing_programmes = self.projects['Kód programu'].unique()

        missing_programmes = [prog for prog in args if prog not in existing_programmes]

        if missing_programmes:
            raise ValueError(f'Programy {missing_programmes} neexistují.')

        else:
            programme_list = [prog for prog in args]
            select_df = self.projects[self.projects['Kód programu'].isin(programme_list)].reset_index(drop=True)
            return Projects(select_df)  # todo maybe another class Programms?

    def select_cfp(self, *args: str) -> 'Projects':
        """ Vyfiltruje tabulku tak, aby obsahovala pouze projekty vybraných veřejných soutěží.

        :param args: kódy veřejných soutěží, které se mají vyfiltrovat
        :return: nová instance třídy Projects s vyfiltrovanými údaji
        :raise: ValueError
        """
        existing_cfp = self.projects['Kód VS'].unique()

        missing_cfp = [cfp for cfp in args if cfp not in existing_cfp]

        if missing_cfp:
            raise ValueError(f'Veřejné soutěže {missing_cfp} neexistují.')

        else:
            cfp_list = [cfp for cfp in args]
            select_df = self.projects[self.projects['Kód VS'].isin(cfp_list)].reset_index(drop=True)
            return Projects(select_df)

    def select_funded(self) -> 'Projects':
        """ Vyfiltruje tabulku tak, aby obsahovala pouze podpořené projekty.

        :return: nová instance třídy Projects s vyfiltrovanými údaji
        """
        funded_states = ['Realizace', 'Implementace', 'Ukončené']
        select_df = self.projects[self.projects['Fáze projektu'].isin(funded_states)].reset_index(drop=True)
        return Projects(select_df)