import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account


class Projects:
    """ Třída, která načítá a reprezentuje tabulku projektů.


       Funguje pouze v rámci Google Colab prostředí.


       :param projects: DataFrame načtených dat ze zdroje pravdy nebo z nově vytvořené (vyfiltrované) instance
       :type projects: DataFrame
       :param summary_cfp: DataFrame s agregovanými údaji na úrovni veřejných soutěží
       :type summary_cfp: DataFrame
       :param summary_prog: DataFrame s agregovanými údaji na úrovni programů
       :type summary_prog: DataFrame
       """

    def __init__(self, df=None):
        """ Kontstruktor, který načte data do DataFrame a vytvoří agregovanou tabulku.
       """
        if df is None:
            self.projects = self._get_projects()
        else:
            self.projects = df
        self.summary_cfp = self.create_summary()
        self.summary_prog = self.create_summary('prog')

    def _get_projects(self) -> pd.DataFrame:
        """ Načte data o projektech z databáze zdroje pravdy v Bigquery.
           Lze použít pouze v rámci Google Colab prostředí.


       :return: DataFrame načtených dat
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
            lambda x: 'Ano' if x['faze_projektu'] in ['Realizace', 'Implementace', 'Ukončené'] else 'Ne', axis=1)
        submitted = temp_df.groupby(['kod_programu', 'kod_VS']).agg(
            {'projectcode': 'count', 'naklady_celkem': 'sum', 'podpora_celkem': 'sum'}).reset_index()
        funded = temp_df[temp_df['Podpořené'] == 'Ano'].groupby(['kod_programu', 'kod_VS']).agg(
            {'projectcode': 'count', 'naklady_celkem': 'sum', 'podpora_celkem': 'sum'}).reset_index()

        summary_df = pd.merge(submitted[['kod_programu', 'kod_VS', 'projectcode']], funded, how='inner',
                              on=['kod_programu', 'kod_VS'])
        summary_df.columns = ['kod_programu', 'kod_VS', 'Podané', 'Podpořené', 'Náklady', 'Podpora']

        if level == 'cfp':
            pass
        elif level == 'prog':
            summary_df = summary_df.groupby('kod_programu').agg('sum', numeric_only=True).reset_index()

        return summary_df

    def select_programme(self, *args: str) -> 'Projects':
        """ Vyfiltruje dataframe projektů tak, aby obsahovala pouze projekty vybraných programů.


       :param args: kódy programů (dvoumístné - například 'FW'), které se mají vyfiltrovat
       :return: nová instance třídy Projects s vyfiltrovanými údaji
       :raise: ValueError
       """

        existing_programmes = self.projects['kod_programu'].unique()

        missing_programmes = [prog for prog in args if prog not in existing_programmes]

        if missing_programmes:
            raise ValueError(f'Programy {missing_programmes} neexistují.')


        else:
            programme_list = [prog for prog in args]
            select_df = self.projects[self.projects['kod_programu'].isin(programme_list)].reset_index(drop=True)
            return Projects(select_df)

    def select_cfp(self, *args: str) -> 'Projects':
        """ Vyfiltruje dataframe projektů tak, aby obsahovala pouze projekty vybraných veřejných soutěží.


       :param args: kódy veřejných soutěží (čtyřmístné - například 'FW01'), které se mají vyfiltrovat
       :return: nová instance třídy Projects s vyfiltrovanými údaji
       :raise: ValueError
       """
        existing_cfp = self.projects['kod_VS'].unique()

        missing_cfp = [cfp for cfp in args if cfp not in existing_cfp]

        if missing_cfp:
            raise ValueError(f'Veřejné soutěže {missing_cfp} neexistují.')


        else:
            cfp_list = [cfp for cfp in args]
            select_df = self.projects[self.projects['kod_VS'].isin(cfp_list)].reset_index(drop=True)
            return Projects(select_df)

    def select_funded(self) -> 'Projects':
        """ Vyfiltruje dataframe projektů tak, aby obsahoval pouze podpořené projekty.


       :return: nová instance třídy Projects s vyfiltrovanými údaji
       """
        funded_states = ['Realizace', 'Implementace', 'Ukončené']
        select_df = self.projects[self.projects['faze_projektu'].isin(funded_states)].reset_index(drop=True)
        return Projects(select_df)


def projects_finance() -> pd.DataFrame:
    """ Načte data o financích projektů z databáze zdroje pravdy v Bigquery.


   Finance jsou v rozdělení po jednotlivých letech.
   Lze použít pouze v rámci Google Colab prostředí.


   :return: DataFrame načtených dat ze zdroje
   """
    credentials = service_account.Credentials.from_service_account_file(
        '/content/drive/Shareddrives/Analytické oddělení/Data/Zdrojová data/data-poc-424211-81ef80050634.json')
    project_id = 'data-poc-424211'
    client = bigquery.Client(credentials=credentials, project=project_id)

    query = """
           SELECT *
           FROM `data-poc-424211.ssot_test.projekty_finance_ssot`
           """
    df = client.query(query).to_dataframe()
    return df
