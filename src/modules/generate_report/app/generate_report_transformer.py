from .generate_report_aggregator import GenerateReportAggregator
import pandas as pd
import io

class GenerateReportTransformer:

    def __init__(self, aggregator: GenerateReportAggregator):
        self.aggregator = aggregator

    def __call__(self, initial_date, final_date):

        user_statistics, court_statistics, sports_statistics = self.aggregator(initial_date, final_date)

        df_users = pd.DataFrame.from_dict(user_statistics, orient="index")
        df_courts = pd.DataFrame.from_dict(court_statistics, orient="index")
        df_sports = pd.DataFrame.from_dict(sports_statistics, orient="index")

        output = io.BytesIO()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_users.to_excel(writer, sheet_name="Usuários")
            df_courts.to_excel(writer, sheet_name="Quadras")
            df_sports.to_excel(writer, sheet_name="Esportes")

        output.seek(0)

        return output

